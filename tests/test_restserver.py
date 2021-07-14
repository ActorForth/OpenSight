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
    transaction_details_with_blockhash,
    transaction_details_with_coinbase,
    block_hash_call_method_node,
    block_hash_electrum_result,
    block_hash_electrum_result_value_satoshi,
    block_hash_electrum_result_without_value,
    block_hash_result,
    block_hash_result_no_reward,
    mocked_post_txid1,
    mocked_post_txid2,
    get_block_details_blockhash,
    get_transaction_details_tx,
    utxo_from_electrum,
)

ADDRESS_ENDPOINT_TEST_ADDRESS = "mofnoitUXBfNFLKqwwomj5KwBVqJeydSyx"

def mock_electrum_connect(*args, **kwargs):
    case = {
        "get_address_details_1": tx_history_1,
        "get_address_details_2": tx_history_balance,
        "get_utxo_for_address_1": address_utxo,
        "get_utxo_for_address_2": address_tx,
        "get_block_details": block_hash_electrum_result,
        "get_block_details_value_satoshi": block_hash_electrum_result_value_satoshi,
    }
    return case.get(kwargs.get("key"), "invalid")

def mock_call_node(*args, **kwargs):
    case = {
        "1": call_node_1,
        "2": call_node_2,
        "transaction_details_1": transaction_call_method_1,
        "transaction_details_2": transaction_call_method_tx,
        "transaction_details_3": transaction_call_method_2,
        "transaction_details_with_blockhash": transaction_details_with_blockhash,
        "transaction_details_with_coinbase": transaction_details_with_coinbase,
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

    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_address_details_exception(self, mock1):
        mock1.side_effect = [
            Exception("get_txs_for_address_error_mock")
        ]

        client = TestClient(app)
        address = ADDRESS_ENDPOINT_TEST_ADDRESS
        url = f"/api/addr/{address}"
        response = client.get(url)
        assert response.json() == {}
        assert response.status_code == 500

    @mock.patch("opensight_restserver.call_method_electrum")
    @mock.patch("opensight_restserver.get_txs_for_address")
    def test_get_address_details_exception_skip_for_if(self, mock1, mock2):
        mock1.side_effect = [
            (
                {
                    "txs": [
                        {"txid": "best_txid", "confirmations": 5},
                        {"txid": "worst_txid", "confirmations": 4},
                        {"txid": "normal_txid", "confirmations": 3},
                        ]
                },
                200
            )
        ]
        mock2.side_effect = [
            tx_history_balance 
        ]

        client = TestClient(app)
        address = ADDRESS_ENDPOINT_TEST_ADDRESS
        url = f"/api/addr/{address}"
        response = client.get(url)
        assert response.json() == {}
        assert response.status_code == 500

    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_utxo_for_address_exception(self, mock1):
        mock1.side_effect = [
            Exception("beat_error")
        ]
        
        client = TestClient(app)
        address = ADDRESS_ENDPOINT_TEST_ADDRESS
        url = f"/api/addr/{address}/utxo"

        response = client.get(url)

        assert response.json() == {}
        assert response.status_code == 500

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
    def test_transaction_details_if_coinbase(self, mock1):
        mock1.side_effect = [
            mock_call_node(key="transaction_details_with_coinbase"),
            mock_call_node(key="transaction_details_2"),
            {"height": 16}
        ]
        transaction = get_transaction_details_tx
        url = f"/api/tx/{transaction}"
        client = TestClient(app)
        response = client.get(url)
        assert response.json() == transaction_details_with_coinbase
        assert response.status_code == 200

    @mock.patch("opensight_restserver.call_method_node")
    def test_transaction_details_if_blockhash(self, mock1):
        mock1.side_effect = [
            mock_call_node(key="transaction_details_with_blockhash"),
            mock_call_node(key="transaction_details_2"),
            {"height": 16}
        ]
        transaction = get_transaction_details_tx
        url = f"/api/tx/{transaction}"
        client = TestClient(app)
        response = client.get(url)
        assert response.json() == transaction_details_with_blockhash
        assert response.status_code == 200

    @mock.patch("opensight_restserver.call_method_node")
    def test_transaction_details_exception(self, mock1):
        mock1.side_effect = [
            Exception
        ]
        transaction = get_transaction_details_tx
        url = f"/api/tx/{transaction}"
        client = TestClient(app)
        response = client.get(url)
        assert response.json() == {}
        assert response.status_code == 500

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
        assert response.json() == block_hash_result

    @mock.patch("opensight_restserver.call_method_electrum")
    @mock.patch("opensight_restserver.call_method_node")
    def test_get_block_details_without_value(self, mock1, mock2):
        mock1.side_effect = [mock_call_node(key="get_block_details")]
        mock2.side_effect = [block_hash_electrum_result_without_value]
        blockhash = get_block_details_blockhash

        url = f"/api/block/{blockhash}"
        client = TestClient(app)
        response = client.get(url)
        assert response.json() == block_hash_result_no_reward

    @mock.patch("opensight_restserver.call_method_electrum")
    @mock.patch("opensight_restserver.call_method_node")
    def test_get_block_details_value_satoshi(self, mock1, mock2):
        mock1.side_effect = [mock_call_node(key="get_block_details")]
        mock2.side_effect = [mock_electrum_connect(key="get_block_details_value_satoshi")]
        blockhash = get_block_details_blockhash

        url = f"/api/block/{blockhash}"
        client = TestClient(app)
        response = client.get(url)
        assert response.json() == block_hash_result

    @mock.patch("opensight_restserver.call_method_node")
    def test_get_block_details_no_block_found(self, mock1):
        mock1.side_effect = [""]
        blockhash = get_block_details_blockhash

        url = f"/api/block/{blockhash}"
        client = TestClient(app)
        response = client.get(url)

        assert response.json() == {'message': 'block id not found'}
        assert response.status_code == 404

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

    @mock.patch("opensight_restserver.call_method_electrum")
    def test_format_utxo_from_electrum(self,mock1):
        mock1.side_effect = [
            mock_electrum_connect(key="get_utxo_for_address_1")
        ]
        utxo = {
            "height": 2,
            "tx_hash": "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce",
            "tx_pos": "0",
            "value": 1000000000,
            "value": 100000000,
        }

        best_block = 10
        address = "mofnoitUXBfNFLKqwwomj5KwBVqJeydSyx"
        p2pkh_script = "76a914596cd4508cd763b019bd4b83e1b4ca0fa58281a688ac"
        response = format_utxo_from_electrum(utxo, best_block, address, p2pkh_script)
        assert response == utxo_from_electrum

    def test_transactions_not_found(self):
        url = "/api/txs/"
        client = TestClient(app)
        response = client.get(url)
        assert response.json() == "address cannot be empty"
        assert response.status_code == 400

    @mock.patch("opensight_restserver.get_txs_for_address")
    def test_transactions_with_mock(self,mock1):
        mock1.side_effect = [
            # mock_electrum_connect(key="get_utxo_for_address_2")
            (address_tx, 200)
        ]
        url = "/api/txs/?address=test_address"
        client = TestClient(app)
        response = client.get(url)
        assert response.json() == address_tx
        assert response.status_code == 200

    @mock.patch("opensight_restserver.call_method_node")
    def test_block_details_retry_exception(self, mock1):
        mock1.side_effect = [
            Exception
        ]

        height = 16
        url = f"/api/block/{height}"
        client = TestClient(app)
        response = client.get(url)
        assert response.json() == {}
        assert response.status_code == 500

