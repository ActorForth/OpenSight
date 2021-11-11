# app.py - a minimal flask api using flask_restful
import hashlib
import json
import logging
import os
import socket
import sys
import time
from decimal import Decimal, getcontext
from functools import wraps

import requests
from cashaddress import convert
from fastapi import FastAPI, Response

getcontext().prec = 8 # Decimal precision
logger = logging.getLogger(__name__)

app = FastAPI()

ELECTRUM_HOST = os.environ.get("ELECTRUM_HOST", "bitcoind-regtest")
ELECTRUM_PORT = int(os.environ.get("ELECTRUM_PORT", 50001))

NODE_RPC_HOST = os.environ.get("NODE_RPC_HOST", "bitcoind-regtest")
NODE_RPC_PORT = int(os.environ.get("NODE_RPC_PORT", 18443))
NODE_RPC_USER = os.environ.get("NODE_RPC_USER", "regtest")
NODE_RPC_PASS = os.environ.get("NODE_RPC_PASS", "regtest")

OPENSIGHT_PORT = os.environ.get("OPENSIGHT_PORT", "3001")

TIMEOUT_DELAY = 0.05
TOTAL_RETRIES = 4
BACKOFF_FACTOR = 2
VERSION = "v1.0.4"

OP_CHECKSIG = b"\xac"
OP_DUP = b"v"
OP_EQUALVERIFY = b"\x88"
OP_HASH160 = b"\xa9"
OP_PUSH_20 = b"\x14"


def retry(exceptions, total_tries=TOTAL_RETRIES, initial_wait=TIMEOUT_DELAY, backoff_factor=BACKOFF_FACTOR, logger=None):
    """
    calling the decorated function applying an exponential backoff.
    Args:
        exceptions: Exception(s) that trigger a retry, can be a tuple
        total_tries: Total tries
        initial_wait: Time to first retry
        backoff_factor: Backoff multiplier (e.g. value of 2 will double the delay each retry).
        logger: logger to be used, if none specified print
    """
    def retry_decorator(f):
        @wraps(f)
        async def func_with_retries(*args, **kwargs):
            _tries, _delay = total_tries + 1, initial_wait
            while _tries > 1:
                _tries -= 1
                try:
                    log(f'{total_tries + 1 - _tries}. try:', logger)
                    result, status = f(*args, **kwargs)
                    log(f'status: {status}', logger)
                    if status in [200, 400, 404, 409]:
                        return result
                except exceptions as e:

                    print_args = args if args else 'no args'
                    if _tries == 1:
                        msg = str(f'Function: {f.__name__}\n'
                                  f'Failed despite best efforts after {total_tries} tries.\n'
                                  f'args: {print_args}, kwargs: {kwargs}')
                        log(msg, logger)
                        raise
                    
                print_args = args if args else 'no args'
                msg = str(f'Function: {f.__name__}\n'
                            f'Retrying in {_delay} seconds!, args: {print_args}, kwargs: {kwargs}\n')
                log(msg, logger)
    
                time.sleep(_delay)
                _delay *= backoff_factor

        return func_with_retries
    return retry_decorator

def log(msg, logger=None):
    if logger:
        logger.warning(msg)
    else:
        print(msg)


def address_to_public_key_hash(address):
    address = convert.to_cash_address(address)
    Address = convert.Address._cash_string(address)
    return bytes(Address.payload)


def script_hash_from_address(address):
    p2pkh_script: bytes = (
        OP_DUP
        + OP_HASH160
        + OP_PUSH_20
        + address_to_public_key_hash(address)
        + OP_EQUALVERIFY
        + OP_CHECKSIG
    )
    script_sha256_reversed: str = (
        hashlib.new("sha256", p2pkh_script).digest()[::-1].hex()
    )

    return (p2pkh_script, script_sha256_reversed)


def connect_to_tcp(host, port):  # pragma: no cover
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    return client


def call_method_node(method, params):
    payload = {"jsonrpc": "1.0", "id": 0, "method": method, "params": params}
    request_headers = {"content-type": "text/plain; "}
    response = requests.post(
        "http://{}:{}@{}:{}".format(
            NODE_RPC_USER, NODE_RPC_PASS, NODE_RPC_HOST, NODE_RPC_PORT
        ),
        headers=request_headers,
        data=json.dumps(payload),
    ).json()

    return dict(response)["result"]


def call_method_electrum(method, params=None, id=0): # pragma: no cover
    # previously had _id as a parameter. changed in code to id
    verb = False # verbose?
    with socket.create_connection((ELECTRUM_HOST, ELECTRUM_PORT), timeout=10.0) as sock:
        def sndrecv(method, params=None):
            outj = { "id" : 0, "jsonrpc" : "2.0", "method" : method, "params": params}
            msg = json.dumps(outj, indent=None).encode("utf8") + b'\n'
            if verb: print(f"Srv --> {msg[:2048]}")
            sock.send(msg)
            resp = bytearray()
            while b'\n' not in resp:
                resp += sock.recv(4096)
            if verb: print(f"Srv <-- {resp[:2048]}")
            j = json.loads(resp.decode("utf8").strip())
            if j.get("error") or j.get("id") != id:
                raise Exception("Error response from Fulcrum:\n\n" + (json.dumps(j.get("error"), indent=4) or j))
            return j.get("result")

        # global ID_NEXT
        # reqid = ID_NEXT; ID_NEXT += 1
        return sndrecv(method, params)


def format_utxo_from_electrum(utxo, best_block, address, p2pkh_script):
    res_utxo = {}
    res_utxo["height"] = utxo["height"]
    res_utxo["txid"] = utxo["tx_hash"]
    res_utxo["vout"] = utxo["tx_pos"]
    res_utxo["satoshis"] = utxo["value"]
    res_utxo["amount"] = utxo["value"] / 100000000.0
    res_utxo["address"] = address
    res_utxo["scriptPubKey"] = p2pkh_script

    # tx = call_method_electrum(
    #     "blockchain.transaction.get",
    #     [utxo['tx_hash'], True]
    # )

    if utxo["height"] == 0:
        res_utxo["confirmations"] = 0
    else:
        res_utxo["confirmations"] = (best_block - utxo["height"]) + 1

    return res_utxo


def format_tx_vin(vin, n):
    if not "coinbase" in vin:
        tx_vout = call_method_node("getrawtransaction", [vin["txid"], True])
        vin["valueSat"] = tx_vout["vout"][vin["vout"]]["value"]
        vin["cashAddress"] = tx_vout["vout"][vin["vout"]]["scriptPubKey"]["addresses"][0]
        vin["doubleSpentTxID"] = None
    vin["n"] = n
    return vin


def format_tx_vout(vout):
    vout["spentTxId"] = None
    vout["spentIndex"] = None
    vout["spentHeight"] = None

    return vout


def get_block_reward(block):
    amount = 0
    coinbase_tx = block["tx"][0]
    tx = call_method_electrum("blockchain.transaction.get", [coinbase_tx, True])

    for vout in tx["vout"]:
        if "value" in vout:
            amount += vout["value"]
        elif "value_satoshi" in vout:
            amount += vout["value_satoshi"]

    return amount / 100000000.0


def get_tx_details(tx_hash):
    try:
        tx = call_method_node("getrawtransaction", [tx_hash, True])
        if not tx:
            return "Not found", 404
        tx["vin"] = [format_tx_vin(vin, n) for n, vin in enumerate(tx["vin"])]
        tx["vout"] = [format_tx_vout(vout) for vout in tx["vout"]]

        tx.pop("hex", None)

        if "coinbase" in tx["vin"][0]:
            tx["valueOut"] = sum([Decimal(str(vout["value"])) for vout in tx["vout"]])
            tx["valueOut"] = float(tx["valueOut"])
        else:
            tx["valueIn"] = sum([Decimal(str(vin["valueSat"])) for vin in tx["vin"]])
            tx["valueOut"] = sum([Decimal(str(vout["value"])) for vout in tx["vout"]])
            tx["fees"] = Decimal(tx["valueIn"]) - Decimal(tx["valueOut"])

            tx["valueIn"] = float(tx["valueIn"])
            tx["valueOut"] = float(tx["valueOut"])
            tx["fees"] = float(tx["fees"])

        if "blockhash" in tx:
            tx["blockheight"] = call_method_node("getblock", [tx["blockhash"]])["height"]
        return tx, 200
    except Exception as e:
        return e, 500


def get_txs_for_address(address):
    try:
        p2pkh_script, script_hash = script_hash_from_address(address)

        tx_history = call_method_electrum(
            "blockchain.scripthash.get_history", [script_hash]
        )
        txs = {}
        txs["txs"] = [get_tx_details(tx["tx_hash"])[0] for tx in tx_history]
        txs["pagesTotal"] = 0
        txs["currentPage"] = 0
        return txs, 200
    except Exception as e:
        return e, 500

@retry(Exception, logger=logger)
async def get_block_details(blockhash):
    try:
        block = call_method_node("getblock", [blockhash, True])
        if not block:
            status = 404 
            return {"message": "block id not found"}, status
        # To investigate
        block["isMainChain"] = True
        block["poolInfo"] = {}

        block["reward"] = get_block_reward(block)
        status = 200
        return block, status
    except Exception as e:
        raise Exception("get_block_error")

@retry(Exception, logger=logger)
async def get_address_utxos(address):
    try:
        p2pkh_script, script_hash = script_hash_from_address(address)

        # Get the UTXOs for the given address
        utxos = call_method_electrum("blockchain.scripthash.listunspent", [script_hash])

        # Get current blockchain height
        best_block = call_method_node("getblockcount", [])
        # Adjust the format of UTXOs to match what rest.bitcoin.com expects
        utxos_formatted = [
            format_utxo_from_electrum(x, best_block, address, p2pkh_script.hex())
            for x in utxos
        ]
        utxos_formatted.reverse()
        return utxos_formatted, 200
    except Exception as e:
        return e, 500

@app.get("/")
async def entry_point(response: Response):
        response.status_code = 200
        return {"platform": "opensight", "version": VERSION}


@retry(Exception, logger=logger)
async def get_address_details(address):
    try:
        p2pkh_script, script_hash = script_hash_from_address(address)

        txs = get_txs_for_address(address)
        if type(txs[0]) is Exception or type(txs[1]) is Exception:
            raise

        if txs[1] != 200:
            return txs[0], txs[1]

        txs = txs[0] #txs is tuple with status_code

        balance = call_method_electrum(
            "blockchain.scripthash.get_balance", [script_hash]
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
            if tx.get("confirmations", 0) <= 0:
                txs_unconfirmed_qty += 1
            for vout in tx["vout"]:
                if p2pkh_script.hex() == vout["scriptPubKey"]["hex"]:
                    total_received = Decimal(total_received) + Decimal(str(vout["value"]))

        total_sent = total_received - Decimal(address_details["balance"])

        address_details["unconfirmedTxApperances"] = txs_unconfirmed_qty
        address_details["totalReceived"] = float(total_received)
        address_details["totalReceivedSat"] = int(total_received * 100000000)
        address_details["totalSent"] = float(total_sent)
        address_details["totalSentSat"] = int(total_sent * 100000000)
        return address_details, 200
    except Exception as e:
        return e, 500

@app.get("/api/addr/{address}")
async def address_details(address, response: Response):
    result, status = await get_address_details(address)
    response.status_code = status
    return result

@app.get("/api/tx/{transaction}")
async def transaction_detail(transaction, response: Response):
    result, status = get_tx_details(transaction)
    response.status_code = status
    return result


@app.get("/api/txs/")
async def transactions(response: Response, address=None, pageNum=None):
    if address==None:
        response.status_code = 400
        return "address cannot be empty"
    result, status = get_txs_for_address(address)
    response.status_code = status
    return result


@app.get("/api/addr/{address}/utxo")
async def address_utxos(address, response: Response):
    result, status = await get_address_utxos(address)
    response.status_code = status
    return result

@app.get("/api/block/{blockhash}")
async def block_details(blockhash, response: Response):
    result, status = await get_block_details(blockhash)
    response.status_code = status
    return result
