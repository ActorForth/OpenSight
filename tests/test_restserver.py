import asyncio
import json
from unittest import mock

import nest_asyncio
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from opensight_restserver import (app, call_method_electrum, format_tx_vin,
                                  format_utxo_from_electrum, get_tx_details,
                                  get_address_details, get_txs_for_address,
                                  TX_BATCH_SIZE, log)

from samples import (address_details, address_result, address_tx, address_utxo,
                     block_hash_call_method_node, block_hash_electrum_result,
                     block_hash_electrum_result_value_satoshi,
                     block_hash_electrum_result_without_value,
                     block_hash_result, block_hash_result_no_reward,
                     call_node_1, call_node_2, get_block_details_blockhash,
                     get_transaction_details_tx, mocked_post_txid1,
                     mocked_post_txid2, transaction_call_method_1,
                     transaction_call_method_2, transaction_call_method_tx,
                     transaction_details_with_blockhash,
                     transaction_details_with_blockhash_response,
                     transaction_details_with_coinbase,
                     transaction_details_with_coinbase_response,
                     transaction_tx_2, tx_history_1, tx_history_balance,
                     utxo_from_electrum)

nest_asyncio.apply()

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
        "get_utxo_for_address": {"result": 229},  # best block
        "empty": 0,
    }
    return case.get(kwargs.get("key"), "invalid")


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    async def json(self):
        return self.json_data

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


def mocked_post(*args, **kwargs):
    # Mocks the post requests to electrum for address balance and txs

    data = kwargs.get("data")
    json_data = json.loads(data)
    if json_data["params"][0] == mocked_post_txid1:
        return MockResponse(call_node_1, 200)
    if json_data["params"][0] == mocked_post_txid2:
        return MockResponse(call_node_2, 200)

    return MockResponse(None, 404)


@pytest.mark.asyncio
class Tests:
    def test_default_endpoint(self):
        with TestClient(app) as client:
            url = "/"
            response = client.get(url)
            assert response.json() == {"platform": "opensight", "version": "v1.0.5"}

    @mock.patch(
        "opensight_restserver.aiohttp.ClientSession.post", side_effect=mocked_post
    )
    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_address_details(self, mock1, mock2):
        mock1.side_effect = [
            mock_electrum_connect(key="get_address_details_1"),
            mock_electrum_connect(key="get_address_details_2"),
        ]

        with TestClient(app) as client:
            address = ADDRESS_ENDPOINT_TEST_ADDRESS
            url = f"/api/addr/{address}"
            response = client.get(url)
            assert response.json() == address_details

    @mock.patch("opensight_restserver.aiohttp.ClientSession.post")
    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_address_details2(self, mock1, mock2):
        mock1.side_effect = [
            mock_electrum_connect(key="get_address_details_1"),
            mock_electrum_connect(key="get_address_details_1"),
            mock_electrum_connect(key="get_address_details_1"),
            mock_electrum_connect(key="get_address_details_1"),
            mock_electrum_connect(key="get_address_details_2"),
        ]
        mock2.side_effect = [
            HTTPException(status_code=500, detail="Timeout"),
            HTTPException(status_code=500, detail="Timeout"),
            HTTPException(status_code=500, detail="Timeout"),
            MockResponse(json_data=call_node_1, status_code=200),
            MockResponse(json_data=call_node_2, status_code=200),
        ]

        with TestClient(app) as client:
            address = ADDRESS_ENDPOINT_TEST_ADDRESS
            url = f"/api/addr/{address}"
            response = client.get(url)
            assert response.json() == address_details

    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_address_details_exception(self, mock1):
        mock1.side_effect = [
            Exception("get_txs_for_address_error_mock"),
            Exception("get_txs_for_address_error_mock"),
            Exception("get_txs_for_address_error_mock"),
            Exception("get_txs_for_address_error_mock"),
        ]
        with pytest.raises(Exception):
            with TestClient(app) as client:
                address = ADDRESS_ENDPOINT_TEST_ADDRESS
                url = f"/api/addr/{address}"
                response = client.get(url)
                assert response.json() == None
                assert response.status_code == 500

    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_utxo_for_address_exception(self, mock1):
        mock1.side_effect = [
            HTTPException(status_code=500, detail="beat_error"),
            HTTPException(status_code=500, detail="beat_error"),
            HTTPException(status_code=500, detail="beat_error"),
            HTTPException(status_code=500, detail="beat_error"),
        ]

        with TestClient(app) as client:
            address = ADDRESS_ENDPOINT_TEST_ADDRESS
            url = f"/api/addr/{address}/utxo"
            response = client.get(url)
            assert response.json() == {"detail": "Error communicating with node"}
            assert response.status_code == 500

    @mock.patch("opensight_restserver.call_method_node")
    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_utxo_for_address(self, mock1, mock2):
        mock1.side_effect = [
            mock_electrum_connect(key="get_utxo_for_address_1"),
            mock_electrum_connect(key="get_utxo_for_address_2"),
        ]
        mock2.side_effect = [mock_call_node(key="get_utxo_for_address")]

        with TestClient(app) as client:
            address = ADDRESS_ENDPOINT_TEST_ADDRESS
            url = f"/api/addr/{address}/utxo"
            response = client.get(url)
            assert response.json() == address_result

    @mock.patch("opensight_restserver.call_method_node")
    def test_transaction_details_if_coinbase(self, mock1):
        mock1.side_effect = [
            mock_call_node(key="transaction_details_with_coinbase"),
            mock_call_node(key="transaction_details_2"),
            {"result": {"height": 16}},
        ]
        transaction = get_transaction_details_tx
        url = f"/api/tx/{transaction}"
        with TestClient(app) as client:
            response = client.get(url)
            assert response.json() == transaction_details_with_coinbase_response
            assert response.status_code == 200

    @mock.patch("opensight_restserver.call_method_node")
    def test_transaction_details_if_blockhash(self, mock1):
        mock1.side_effect = [
            mock_call_node(key="transaction_details_with_blockhash"),
            mock_call_node(key="transaction_details_2"),
            {"result": {"height": 16}},
        ]
        transaction = get_transaction_details_tx
        url = f"/api/tx/{transaction}"
        with TestClient(app) as client:
            response = client.get(url)
            assert response.json() == transaction_details_with_blockhash_response
            assert response.status_code == 200

    @mock.patch("opensight_restserver.call_method_node")
    def test_transaction_details_exception(self, mock1):
        mock1.side_effect = [
            Exception,
            Exception,
            Exception,
            Exception,
        ]
        transaction = get_transaction_details_tx
        with pytest.raises(Exception):
            url = f"/api/tx/{transaction}"
            with TestClient(app) as client:
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
        with TestClient(app) as client:
            response = client.get(url)
            assert response.json() == transaction_tx_2

    @mock.patch("opensight_restserver.call_method_electrum")
    @mock.patch("opensight_restserver.call_method_node")
    def test_get_block_details(self, mock1, mock2):
        mock1.side_effect = [mock_call_node(key="get_block_details")]
        mock2.side_effect = [mock_electrum_connect(key="get_block_details")]
        blockhash = get_block_details_blockhash

        url = f"/api/block/{blockhash}"
        with TestClient(app) as client:
            response = client.get(url)
            assert response.json() == block_hash_result

    @mock.patch("opensight_restserver.call_method_electrum")
    @mock.patch("opensight_restserver.call_method_node")
    def test_get_block_details_without_value(self, mock1, mock2):
        mock1.side_effect = [mock_call_node(key="get_block_details")]
        mock2.side_effect = [block_hash_electrum_result_without_value]
        blockhash = get_block_details_blockhash

        url = f"/api/block/{blockhash}"
        with TestClient(app) as client:
            response = client.get(url)
            assert response.json() == block_hash_result_no_reward

    @mock.patch("opensight_restserver.call_method_electrum")
    @mock.patch("opensight_restserver.call_method_node")
    def test_get_block_details_value_satoshi(self, mock1, mock2):
        mock1.side_effect = [mock_call_node(key="get_block_details")]
        mock2.side_effect = [
            mock_electrum_connect(key="get_block_details_value_satoshi")
        ]
        blockhash = get_block_details_blockhash

        url = f"/api/block/{blockhash}"
        with TestClient(app) as client:
            response = client.get(url)
            assert response.json() == block_hash_result

    @mock.patch("opensight_restserver.call_method_node")
    async def test_get_block_details_no_block_found(self, mock1):
        mock1.side_effect = [""]
        blockhash = get_block_details_blockhash

        url = f"/api/block/{blockhash}"
        with TestClient(app) as client:
            response = client.get(url)
            assert response.json() == {"message": "block id not found"}
            assert response.status_code == 404


    @mock.patch("opensight_restserver.call_method_node")
    async def test_get_tx_details_404(self, mock1):
        mock1.side_effect = [mock_call_node(key="empty")]
        result, status = await get_tx_details("thank", None, None)
        assert result == "Not found"
        assert status == 404

    @mock.patch("opensight_restserver.call_method_electrum")
    def test_format_utxo_from_electrum(self, mock1):
        mock1.side_effect = [mock_electrum_connect(key="get_utxo_for_address_1")]
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
        with TestClient(app) as client:
            response = client.get(url)
            assert response.json() == "address cannot be empty"
            assert response.status_code == 400

    @mock.patch("opensight_restserver.get_txs_for_address")
    def test_transactions_with_mock(self, mock1):
        mock1.side_effect = [
            # mock_electrum_connect(key="get_utxo_for_address_2")
            (address_tx, 200)
        ]
        url = "/api/txs/?address=test_address"
        with TestClient(app) as client:
            response = client.get(url)
            assert response.json() == address_tx
            assert response.status_code == 200

    @mock.patch("opensight_restserver.call_method_node")
    def test_block_details_retry_exception(self, mock1):
        mock1.side_effect = [
            Exception,
            Exception,
            Exception,
            Exception,
        ]

        height = 16
        url = f"/api/block/{height}"
        with TestClient(app) as client:
            response = client.get(url)
            assert response.json() == {"detail": "Error communicating with node"}
            assert response.status_code == 500

    @mock.patch("opensight_restserver.asyncio.open_connection")
    async def test_call_method_electrum_success(self, mock_conn):
        """Test async electrum call returns result correctly."""
        response_data = {"id": 0, "jsonrpc": "2.0", "result": {"confirmed": 1000, "unconfirmed": 0}}
        response_bytes = json.dumps(response_data).encode("utf8") + b"\n"

        mock_reader = mock.AsyncMock()
        mock_reader.read = mock.AsyncMock(return_value=response_bytes)
        mock_writer = mock.AsyncMock()
        mock_writer.close = mock.Mock()
        mock_writer.wait_closed = mock.AsyncMock()

        mock_conn.return_value = (mock_reader, mock_writer)

        result = await call_method_electrum("blockchain.address.get_balance", ["test_addr"])
        assert result == {"confirmed": 1000, "unconfirmed": 0}
        mock_writer.write.assert_called_once()
        mock_writer.close.assert_called_once()

    @mock.patch("opensight_restserver.asyncio.open_connection")
    async def test_call_method_electrum_error_response(self, mock_conn):
        """Test async electrum call raises on error response."""
        response_data = {"id": 0, "jsonrpc": "2.0", "error": {"code": -1, "message": "not found"}}
        response_bytes = json.dumps(response_data).encode("utf8") + b"\n"

        mock_reader = mock.AsyncMock()
        mock_reader.read = mock.AsyncMock(return_value=response_bytes)
        mock_writer = mock.AsyncMock()
        mock_writer.close = mock.Mock()
        mock_writer.wait_closed = mock.AsyncMock()

        mock_conn.return_value = (mock_reader, mock_writer)

        with pytest.raises(Exception, match="Error response from Fulcrum"):
            await call_method_electrum("blockchain.address.get_balance", ["bad_addr"])
        mock_writer.close.assert_called_once()

    @mock.patch("opensight_restserver.asyncio.open_connection")
    async def test_call_method_electrum_connection_closed(self, mock_conn):
        """Test async electrum call handles premature connection close."""
        mock_reader = mock.AsyncMock()
        mock_reader.read = mock.AsyncMock(return_value=b"")
        mock_writer = mock.AsyncMock()
        mock_writer.close = mock.Mock()
        mock_writer.wait_closed = mock.AsyncMock()

        mock_conn.return_value = (mock_reader, mock_writer)

        with pytest.raises(Exception):
            await call_method_electrum("blockchain.address.get_balance", ["test_addr"])
        mock_writer.close.assert_called_once()

    @mock.patch("opensight_restserver.get_tx_details")
    @mock.patch("opensight_restserver.call_method_electrum")
    async def test_get_txs_for_address_batching(self, mock_electrum, mock_get_tx):
        """Test that get_txs_for_address processes in batches."""
        num_txs = TX_BATCH_SIZE + 5
        tx_history = [{"tx_hash": f"hash_{i}"} for i in range(num_txs)]
        mock_electrum.return_value = tx_history
        mock_get_tx.return_value = ({"txid": "test", "vin": [], "vout": []}, 200)

        result, status = await get_txs_for_address("test_addr", None, asyncio.Semaphore(100))
        assert status == 200
        assert len(result["txs"]) == num_txs
        assert mock_get_tx.call_count == num_txs

    @mock.patch("opensight_restserver.aiohttp.ClientSession.post", side_effect=mocked_post)
    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_address_details_with_unconfirmed(self, mock_electrum, mock_post):
        """Test address details with unconfirmed transactions (covers line 448->450)."""
        # tx_history with one tx
        unconfirmed_tx_history = [{"tx_hash": mocked_post_txid1}]
        # balance with unconfirmed
        unconfirmed_balance = {"confirmed": 0, "unconfirmed": 100000000}

        mock_electrum.side_effect = [
            unconfirmed_tx_history,  # get_history
            unconfirmed_balance,  # get_balance
        ]

        with TestClient(app) as client:
            url = f"/api/addr/{ADDRESS_ENDPOINT_TEST_ADDRESS}"
            response = client.get(url)
            assert response.status_code == 200
            data = response.json()
            assert data["unconfirmedBalanceSat"] == 100000000

    @mock.patch("opensight_restserver.call_method_electrum")
    def test_retry_exhaustion_returns_500(self, mock_electrum):
        """Test that retry exhaustion returns proper error (covers lines 103-112)."""
        mock_electrum.side_effect = [
            HTTPException(status_code=500, detail="fail"),
            HTTPException(status_code=500, detail="fail"),
            HTTPException(status_code=500, detail="fail"),
            HTTPException(status_code=500, detail="fail"),
            HTTPException(status_code=500, detail="fail"),
        ]

        with TestClient(app) as client:
            url = f"/api/addr/{ADDRESS_ENDPOINT_TEST_ADDRESS}/utxo"
            response = client.get(url)
            assert response.status_code == 500
            assert response.json() == {"detail": "Error communicating with node"}

    @mock.patch("opensight_restserver.get_txs_for_address")
    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_address_details_txs_non_200(self, mock_electrum, mock_txs):
        """Test address details when get_txs_for_address returns non-200 (covers line 427)."""
        mock_txs.return_value = ({"error": "not found"}, 404)

        with TestClient(app) as client:
            url = f"/api/addr/{ADDRESS_ENDPOINT_TEST_ADDRESS}"
            response = client.get(url)
            assert response.status_code == 404
            assert response.json() == {"error": "not found"}

    @mock.patch("opensight_restserver.asyncio.open_connection")
    async def test_call_method_electrum_wait_closed_exception(self, mock_conn):
        """Test that writer cleanup handles wait_closed exceptions (covers lines 225-226)."""
        response_data = {"id": 0, "jsonrpc": "2.0", "result": []}
        response_bytes = json.dumps(response_data).encode("utf8") + b"\n"

        mock_reader = mock.AsyncMock()
        mock_reader.read = mock.AsyncMock(return_value=response_bytes)
        mock_writer = mock.AsyncMock()
        mock_writer.close = mock.Mock()
        mock_writer.wait_closed = mock.AsyncMock(side_effect=ConnectionResetError("reset"))

        mock_conn.return_value = (mock_reader, mock_writer)

        result = await call_method_electrum("blockchain.address.listunspent", ["test"])
        assert result == []
        mock_writer.close.assert_called_once()

    @mock.patch("opensight_restserver.call_method_electrum")
    @mock.patch("opensight_restserver.get_txs_for_address")
    def test_get_address_details_all_confirmed(self, mock_txs, mock_electrum):
        """Test address details where all txs are confirmed (covers branch 448->450)."""
        # Mock txs with confirmed transactions (confirmations > 0)
        mock_txs.return_value = (
            {
                "txs": [
                    ({"txid": "abc123", "confirmations": 10, "vout": [
                        {"value": 1.0, "scriptPubKey": {"hex": "76a914596cd4508cd763b019bd4b83e1b4ca0fa58281a688ac"}}
                    ]}, 200),
                ],
                "pagesTotal": 0,
                "currentPage": 0,
            },
            200,
        )
        mock_electrum.return_value = {"confirmed": 100000000, "unconfirmed": 0}

        with TestClient(app) as client:
            url = f"/api/addr/{ADDRESS_ENDPOINT_TEST_ADDRESS}"
            response = client.get(url)
            assert response.status_code == 200
            data = response.json()
            assert data["unconfirmedTxAppearances"] == 0
            assert data["unconfirmedBalanceSat"] == 0
