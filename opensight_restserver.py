# app.py - a minimal flask api using flask_restful
import hashlib
import json
import socket

import requests
from cashaddress import convert
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

ELECTRUM_HOST = "bitcoind-regtest"
ELECTRUM_PORT = 50001

NODE_RPC_HOST = "bitcoind-regtest"
NODE_RPC_PORT = 18332
NODE_RPC_USER = "regtest"
NODE_RPC_PASS = "regtest"


OP_CHECKSIG = b'\xac'
OP_DUP = b'v'
OP_EQUALVERIFY = b'\x88'
OP_HASH160 = b'\xa9'
OP_PUSH_20 = b'\x14'


def address_to_public_key_hash(address):
    address = convert.to_cash_address(address)
    Address = convert.Address._cash_string(address)
    return bytes(Address.payload)


def script_hash_from_address(address):
    p2pkh_script: bytes = (
        OP_DUP +
        OP_HASH160 +
        OP_PUSH_20 +
        address_to_public_key_hash(address) +
        OP_EQUALVERIFY +
        OP_CHECKSIG
    )
    script_sha256_reversed: str = hashlib.new(
        'sha256',
        p2pkh_script
    ).digest()[::-1].hex()

    return (p2pkh_script, script_sha256_reversed)


def connect_to_tcp(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    return client


def call_method_node(method, params):
    payload = {
        "jsonrpc": "1.0",
        "id": 0,
        "method": method,
        "params": params
    }
    request_headers = {'content-type': 'text/plain; '}

    response = requests.post(
        "http://{}:{}@{}:{}".format(NODE_RPC_USER, NODE_RPC_PASS, NODE_RPC_HOST, NODE_RPC_PORT),
        headers=request_headers,
        data=json.dumps(payload)
    ).json()

    return dict(response)["result"]


def call_method_electrum(method, params):
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }

    client = connect_to_tcp(ELECTRUM_HOST, ELECTRUM_PORT)

    client.sendall(bytes(json.dumps(payload) + "\n", "ascii"))

    response = client.recv(999999999)
    client.close()

    return dict(json.loads(response.decode()))['result']


def format_utxo_from_electrum(utxo, address, p2pkh_script):
    res_utxo = {}
    res_utxo['height'] = utxo['height']
    res_utxo['txid'] = utxo['tx_hash']
    res_utxo['height'] = utxo['tx_hash']
    res_utxo['vout'] = utxo['tx_pos']
    res_utxo['satoshis'] = utxo['value']
    res_utxo['amount'] = utxo['value'] / 100000000.0
    res_utxo['address'] = address
    res_utxo['scriptPubKey'] = p2pkh_script

    tx = call_method_electrum(
        "blockchain.transaction.get",
        [utxo['tx_hash'], True]
    )

    res_utxo['confirmations'] = tx['confirmations']

    return res_utxo


def format_tx_vin(vin, n):
    tx_vout = call_method_node(
        "getrawtransaction",
        [vin["txid"], True]
    )
    vin["value"] = tx_vout["vout"][vin["vout"]]["value"]
    vin["n"] = n
    vin["doubleSpentTxID"] = None
    return vin


def format_tx_vout(vout):
    vout["spentTxId"] = None
    vout["spentIndex"] = None
    vout["spentHeight"] = None

    return vout


def get_block_reward(block):
    amount = 0
    coinbase_tx = block['tx'][0]
    tx = call_method_electrum('blockchain.transaction.get', [coinbase_tx, True])

    for vout in tx['vout']:
        amount += vout['value']

    return (amount / 100000000.0)


def get_tx_details(tx_hash):
    tx = call_method_node(
        "getrawtransaction",
        [tx_hash, True]
    )
    tx["vin"] = [format_tx_vin(vin, n) for n, vin in enumerate(tx["vin"])]
    tx["vout"] = [format_tx_vout(vout) for vout in tx["vout"]]

    tx.pop('hex', None)

    tx["valueIn"] = sum([vin["value"] for vin in tx["vin"]])
    tx["valueOut"] = sum([vout["value"] for vout in tx["vout"]])

    tx["fees"] = tx["valueIn"] - tx["valueOut"]

    if "blockhash" in tx:
        tx["blockheight"] = call_method_node(
            "getblock",
            [tx["blockhash"]]
        )["height"]
    return tx


def get_txs_for_address(address):
    p2pkh_script, script_hash = script_hash_from_address(address)

    tx_history = call_method_electrum(
        "blockchain.scripthash.get_history",
        [script_hash]
    )

    txs = {}
    txs["txs"] = [get_tx_details(tx["tx_hash"]) for tx in tx_history]
    txs["pagesTotal"] = 0
    txs["currentPage"] = 0

    return txs


class EntryPoint(Resource):
    def get(self):
        return {'hello': 'world'}


class AddressDetail(Resource):
    def get(self, address):
        p2pkh_script, script_hash = script_hash_from_address(address)

        txs = get_txs_for_address(address)

        balance = call_method_electrum(
            "blockchain.scripthash.get_balance",
            [script_hash]
        )

        address_details = {}
        total_balance = balance["confirmed"] + balance["unconfirmed"]

        address_details["addrStr"] = address
        address_details["balanceSat"] = total_balance
        address_details["unconfirmedBalanceSat"] = balance["unconfirmed"]

        address_details["balance"] = total_balance / 100000000.0
        address_details["unconfirmedBalance"] = balance["unconfirmed"] / 100000000.0

        address_details["transactions"] = [tx["txid"] for tx in txs["txs"]]
        address_details["txApperances"] = len(address_details["transactions"])

        total_received = 0
        txs_unconfirmed_qty = 0
        for tx in txs["txs"]:
            if tx["confirmations"] <= 0:
                txs_unconfirmed_qty += 1
            for vout in tx["vout"]:
                if p2pkh_script.hex() == vout["scriptPubKey"]["hex"]:
                    total_received += vout["value"]

        total_sent = total_received - address_details["balance"]

        address_details["unconfirmedTxApperances"] = txs_unconfirmed_qty
        address_details["totalReceived"] = total_received
        address_details["totalReceivedSat"] = int(total_received * 100000000)
        address_details["totalSent"] = total_sent
        address_details["totalSentSat"] = int(total_sent * 100000000)

        return address_details


class TransactionDetail(Resource):
    def get(self, transaction):
        return get_tx_details(transaction)


class Transactions(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('address', type=str)
        parser.add_argument('pageNum', type=str)

        args = parser.parse_args()

        return get_txs_for_address(args["address"])


class AddressUtxos(Resource):
    def get(self, address):
        p2pkh_script, script_hash = script_hash_from_address(address)

        utxos = call_method_electrum(
            "blockchain.scripthash.listunspent",
            [script_hash]
        )

        utxos_formatted = [
            format_utxo_from_electrum(x, address, p2pkh_script.hex())
            for x in utxos
        ]

        return utxos_formatted


class BlockDetails(Resource):
    def get(self, blockhash):

        block = call_method_node("getblock", [blockhash, True])

        # To investigate
        block["isMainChain"] = True
        block["poolInfo"] = {}

        block["reward"] = get_block_reward(block)

        return block


api.add_resource(EntryPoint, '/')
api.add_resource(AddressDetail, '/api/addr/<address>')
api.add_resource(TransactionDetail, '/api/tx/<transaction>')
api.add_resource(Transactions, '/api/txs/')
api.add_resource(AddressUtxos, '/api/addr/<address>/utxo')
api.add_resource(BlockDetails, '/api/block/<blockhash>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='3001')
