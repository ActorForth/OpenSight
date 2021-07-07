from unittest import mock
import json
from fastapi.testclient import TestClient
import logging

from opensight_restserver import app, format_tx_vin, format_utxo_from_electrum, get_tx_details, log
from samples import (
    tx_history_1,
    tx_history_balance,
    call_node_1,
    call_node_2,
    address_details,
    address_utxo,
    address_tx,
    address_result,
    transaction_tx_2,
    transaction_call_method_1,
    transaction_call_method_tx,
    transaction_call_method_2,
    block_hash_call_method_node,
    block_hash_electrum_result,
    block_hash_result,
    mocked_post_txid1,
    mocked_post_txid2,
    get_block_details_blockhash,
    get_transaction_details_tx
)

ADDRESS_ENDPOINT_TEST_ADDRESS = "mofnoitUXBfNFLKqwwomj5KwBVqJeydSyx"

def mock_electrum_connect(*args, **kwargs):
    case = {
        "get_address_details_1": tx_history_1,
        "get_address_details_2": tx_history_balance,
        "get_utxo_for_address_1": address_utxo,
        "get_utxo_for_address_2": address_tx,
        "get_block_details": block_hash_electrum_result,
    }
    return case.get(kwargs.get("key"), "invalid")

def mock_call_node(*args, **kwargs):
    case = {
        "1": call_node_1,
        "2": call_node_2,
        "transaction_details_1": transaction_call_method_1,
        "transaction_details_2": transaction_call_method_tx,
        "transaction_details_3": transaction_call_method_2,
        "get_block_details": block_hash_call_method_node,
        "get_utxo_for_address": 229,  # best block
        "empty": 0
    }
    return case.get(kwargs.get("key"), "invalid")

def mocked_post(*args, **kwargs):
    # Mocks the post requests to electrum for address balance and txs
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    data = kwargs.get("data")
    json_data = json.loads(data)

    if (
        json_data["params"][0]
        == mocked_post_txid1
    ):
        return MockResponse(call_node_1, 200)
    if (
        json_data["params"][0]
        == mocked_post_txid2
    ):
        return MockResponse(call_node_2, 200)

    return MockResponse(None, 404)


class Tests:
    def test_default_endpoint(self):
        client = TestClient(app)
        url = "/"
        response = client.get(url)
        assert response.json() == {'platform': 'opensight', 'version': 'v1.0.4'}

    @mock.patch("opensight_restserver.requests.post", side_effect=mocked_post)
    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_address_details(self, mock1, mock2):
        mock1.side_effect = [
            mock_electrum_connect(key="get_address_details_1"),
            mock_electrum_connect(key="get_address_details_2"),
        ]

        client = TestClient(app)
        address = ADDRESS_ENDPOINT_TEST_ADDRESS
        url = f"/api/addr/{address}"
        response = client.get(url)
        assert response.json() == address_details

    @mock.patch("opensight_restserver.call_method_node")
    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_utxo_for_address(self, mock1, mock2):
        mock1.side_effect = [
            mock_electrum_connect(key="get_utxo_for_address_1"),
            mock_electrum_connect(key="get_utxo_for_address_2"),
        ]
        mock2.side_effect = [
            mock_call_node(key="get_utxo_for_address")
        ]
        
        client = TestClient(app)
        address = ADDRESS_ENDPOINT_TEST_ADDRESS
        url = f"/api/addr/{address}/utxo"

        response = client.get(url)

        assert response.json() == address_result

    @mock.patch("opensight_restserver.call_method_node")
    def test_transaction_details(self, mock1):
        mock1.side_effect = [
            mock_call_node(key="transaction_details_1"),
            mock_call_node(key="transaction_details_2"),
            mock_call_node(key="transaction_details_3"),
        ]
        transaction = get_transaction_details_tx
        url = f"/api/tx/{transaction}"
        client = TestClient(app)
        response = client.get(url)
        print(response.json())
        assert response.json() == transaction_tx_2


    @mock.patch("opensight_restserver.call_method_electrum")
    @mock.patch("opensight_restserver.call_method_node")
    def test_get_block_details(self, mock1, mock2):
        mock1.side_effect = [mock_call_node(key="get_block_details")]
        mock2.side_effect = [mock_electrum_connect(key="get_block_details")]
        blockhash = get_block_details_blockhash

        url = f"/api/block/{blockhash}"
        client = TestClient(app)
        response = client.get(url)
        print(response.json())
        assert response.json() == block_hash_result

    def test_log_if(self):
        log("beat_test_log_lol_>////<")

    def test_log_else(self):
        logger = logging.getLogger(__name__)
        log("beat_test_log_lol_>////<", logger)

    @mock.patch("opensight_restserver.call_method_node")
    def test_get_tx_details_404(self, mock1):
        mock1.side_effect = [
            mock_call_node(key = "empty")
        ]
        result, status = get_tx_details("thank")
        assert result == "Not found"
        assert status == 404

    @mock.patch("opensight_restserver.call_method_node")
    def test_format_tx_vin(self, mock1):
        mock1.side_effect = [
            mock_call_node(key="transaction_details_2")
        ]
        vin = {
            "coinbase": " ",
            "txid": " ",
            "valueSat": " ",
            "vout": 0,
            "value": " ",
            "cashAddress": " ",
            "scriptPubKey": " ",
            "addresses": " ",
            "doubleSpentTxID": " "
        }
        n = " "
        format_tx_vin(vin, n)

    @mock.patch("opensight_restserver.call_method_electrum")
    def test_format_utxo_from_electrum(self,mock1):
        mock1.side_effect = [
            mock_electrum_connect(key="get_utxo_for_address_1")
        ]
        utxo = {
            "height": 2,
            "tx_hash": " ",
            "tx_pos": " ",
            "value": 1000000000,
            "value": 100000000,
        }
        best_block = 10
        address = " "
        p2pkh_script = " "
        format_utxo_from_electrum(utxo, best_block, address, p2pkh_script)

    def test_transactions_not_found(self):
        url = "/api/txs/"
        client = TestClient(app)
        response = client.get(url)
        assert response.json() == "address cannot be empty"
        assert response.status_code == 400