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
    block_hash_result
)


def mock_electrum_connect(*args, **kwargs):
    case = {
        "1" : tx_history_1,
        "2" : tx_history_balance,
        "3" : address_utxo,
        "4" : address_tx,
        "5" : block_hash_electrum_result
        }
    a = case.get(kwargs.get("key"), "invalid")
    return a

def mock_call_node(*args, **kwargs):
    case = {
        "1": call_node_1,
        "2": call_node_2,
        "3": transaction_call_method_1,
        "4": transaction_call_method_tx,
        "5": transaction_call_method_2,
        "6": block_hash_call_method_node,
        "7": 229,  # best block
        }
    a = case.get(kwargs.get("key"), "invalid")
    return a


def mocked_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    
    data = kwargs.get("data")
    json_data = json.loads(data)
    
    
    if json_data["params"][0] == "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce":
        return MockResponse(call_node_1, 200)
    if json_data["params"][0] == "0034e7c1eac32cdcb0b2098a33f488a8ee1b814846996e786ca92f5a60fd2148":
        return MockResponse(call_node_2, 200)
    

    return MockResponse(None, 404)

class Tests:

    def test_default_entry(self):
        flask_app = app

        with flask_app.test_client(self) as test_client:
           
            data = {
            }

            response = test_client.get(
                "/", content_type="application/json"
            )

            result = json.loads(response.get_data(as_text=True))
            assert result == {'platform': 'opensight', 'version': '0.1.1'}


    @mock.patch("opensight_restserver.requests.post", side_effect=mocked_post)
    @mock.patch("opensight_restserver.call_method_electrum")
    def test_addr(self, mock1, mock2):
        mock1.side_effect = [
            mock_electrum_connect(key="1"),
            mock_electrum_connect(key="2")
        ]

        flask_app = app

        with flask_app.test_client(self) as test_client:
           
            address = "mofnoitUXBfNFLKqwwomj5KwBVqJeydSyx"
            url = f"/api/addr/{address}"
            response = test_client.get(
                url, content_type="application/json"
            )

            result = json.loads(response.get_data(as_text=True))
            assert result == address_details
    
    @mock.patch("opensight_restserver.call_method_node")
    @mock.patch("opensight_restserver.call_method_electrum")
    def test_addr_utxo(self, mock1, mock2):
        mock1.side_effect = [
            mock_electrum_connect(key="3"),
            mock_electrum_connect(key="4")
        ]
        mock2.side_effect = [
            mock_call_node(key="7")
        ]
        flask_app = app
        
        with flask_app.test_client(self) as test_client:
            address = "mofnoitUXBfNFLKqwwomj5KwBVqJeydSyx"
            url = f"/api/addr/{address}/utxo"

            response = test_client.get(url, content_type="application/json")

            result = json.loads(response.get_data(as_text=True))

            assert result == address_result

    @mock.patch("opensight_restserver.call_method_node")
    def test_transaction(self, mock1):
        mock1.side_effect = [
            mock_call_node(key="3"),
            mock_call_node(key="4"),
            mock_call_node(key="5"),
        ]
        transaction = "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce"
        url = f"/api/tx/{transaction}"
        flask_app = app
        with flask_app.test_client(self) as test_client:
            response = test_client.get(url, content_type="application/json")

            result = json.loads(response.get_data(as_text=True))
            assert result == transaction_tx

    @mock.patch("opensight_restserver.call_method_electrum")
    @mock.patch("opensight_restserver.call_method_node")
    def test_txs(self, mock1, mock2):
        mock1.side_effect=[
            mock_call_node(key="6")
        ]
        mock2.side_effect = [
            mock_electrum_connect(key="5")
        ]
        blockhash = "0c4339894f7aadb14884c259fbb177b6bea5a063b1c52d537aa7d0bd378827cf"

        url = f"/api/block/{blockhash}"

        flask_app = app
        with flask_app.test_client(self) as test_client:
            response = test_client.get(url, content_type="application/json")

            result = json.loads(response.get_data(as_text=True))
            assert result == block_hash_result
            