import pytest
import unittest
from unittest import mock
from unittest.mock import mock_open

# import requests_mock
from flask import json, current_app, jsonify
import os
import time
import threading

import sys
from opensight_restserver import app
from samples import (
    tx_history_1,
    tx_history_balance,
    call_node_1,
    call_node_2,
    address_details,
    address_utxo,
    address_tx,
    address_result,
    transaction_tx,
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
        flask_app = app

        with flask_app.test_client(self) as test_client:

            data = {}

            response = test_client.get("/", content_type="application/json")

            result = json.loads(response.get_data(as_text=True))
            assert result == {"platform": "opensight", "version": "0.1.1"}

    @mock.patch("opensight_restserver.requests.post", side_effect=mocked_post)
    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_address_details(self, mock1, mock2):
        mock1.side_effect = [
            mock_electrum_connect(key="get_address_details_1"),
            mock_electrum_connect(key="get_address_details_2"),
        ]

        flask_app = app

        with flask_app.test_client(self) as test_client:

            address = ADDRESS_ENDPOINT_TEST_ADDRESS
            url = f"/api/addr/{address}"
            response = test_client.get(url, content_type="application/json")

            result = json.loads(response.get_data(as_text=True))
            assert result == address_details

    @mock.patch("opensight_restserver.call_method_node")
    @mock.patch("opensight_restserver.call_method_electrum")
    def test_get_utxo_for_address(self, mock1, mock2):
        mock1.side_effect = [
            mock_electrum_connect(key="get_utxo_for_address_1"),
            mock_electrum_connect(key="get_utxo_for_address_2"),
        ]
        mock2.side_effect = [mock_call_node(key="get_utxo_for_address")]
        flask_app = app

        with flask_app.test_client(self) as test_client:
            address = ADDRESS_ENDPOINT_TEST_ADDRESS
            url = f"/api/addr/{address}/utxo"

            response = test_client.get(url, content_type="application/json")

            result = json.loads(response.get_data(as_text=True))

            assert result == address_result

    @mock.patch("opensight_restserver.call_method_node")
    def test_transaction_details(self, mock1):
        mock1.side_effect = [
            mock_call_node(key="transaction_details_1"),
            mock_call_node(key="transaction_details_2"),
            mock_call_node(key="transaction_details_3"),
        ]
        transaction = get_transaction_details_tx
        url = f"/api/tx/{transaction}"
        flask_app = app
        with flask_app.test_client(self) as test_client:
            response = test_client.get(url, content_type="application/json")

            result = json.loads(response.get_data(as_text=True))
            assert result == transaction_tx

    @mock.patch("opensight_restserver.call_method_electrum")
    @mock.patch("opensight_restserver.call_method_node")
    def test_get_block_details(self, mock1, mock2):
        mock1.side_effect = [mock_call_node(key="get_block_details")]
        mock2.side_effect = [mock_electrum_connect(key="get_block_details")]
        blockhash = get_block_details_blockhash

        url = f"/api/block/{blockhash}"

        flask_app = app
        with flask_app.test_client(self) as test_client:
            response = test_client.get(url, content_type="application/json")

            result = json.loads(response.get_data(as_text=True))
            assert result == block_hash_result
