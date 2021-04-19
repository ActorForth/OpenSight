tx_history_1 = [
    {
        "fee": 226,
        "height": 0,
        "tx_hash": "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce",
    }
]

tx_history_balance = {"confirmed": 0, "unconfirmed": 100000000}

call_node_1_params = [
    "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce",
    True,
]
call_node_1 = {
    "result": {
        "txid": "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce",
        "size": 225,
        "version": 1,
        "locktime": 229,
        "vin": [
            {
                "txid": "0034e7c1eac32cdcb0b2098a33f488a8ee1b814846996e786ca92f5a60fd2148",
                "vout": 1,
                "scriptSig": {
                    "asm": "304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24[ALL|FORKID] 02498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260",
                    "hex": "47304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24412102498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260",
                },
                "sequence": 4294967294,
            }
        ],
        "vout": [
            {
                "value": 1.0,
                "n": 0,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 596cd4508cd763b019bd4b83e1b4ca0fa58281a6 OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a914596cd4508cd763b019bd4b83e1b4ca0fa58281a688ac",
                    "reqSigs": 1,
                    "type": "pubkeyhash",
                    "addresses": ["bchreg:qpvke4zs3ntk8vqeh49c8cd5eg86tq5p5cxqce75q9"],
                },
            },
            {
                "value": 46.99999356,
                "n": 1,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 15b3fba239bc86328d55507cfff76b1447de710c OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a91415b3fba239bc86328d55507cfff76b1447de710c88ac",
                    "reqSigs": 1,
                    "type": "pubkeyhash",
                    "addresses": ["bchreg:qq2m87az8x7gvv5d24g8ellhdv2y0hn3psamm0pptx"],
                },
            },
        ],
        "confirmations": 0,
        "time": 1615799934,
        "hex": "01000000014821fd605a2fa96c786e994648811beea888f4338a09b2b0dc2cc3eac1e73400010000006a47304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24412102498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260feffffff0200e1f505000000001976a914596cd4508cd763b019bd4b83e1b4ca0fa58281a688ac7c4c2418010000001976a91415b3fba239bc86328d55507cfff76b1447de710c88ace5000000",
    },
    "error": None,
    "id": 0,
}

call_node_2_params = [
    "0034e7c1eac32cdcb0b2098a33f488a8ee1b814846996e786ca92f5a60fd2148",
    True,
]
call_node_2 = {
    "result": {
        "txid": "0034e7c1eac32cdcb0b2098a33f488a8ee1b814846996e786ca92f5a60fd2148",
        "size": 226,
        "version": 1,
        "locktime": 223,
        "vin": [
            {
                "txid": "54a3934bd6b06776e1519d27954556b256b2b01c7d26285e209352df48670177",
                "vout": 1,
                "scriptSig": {
                    "asm": "3045022100dd59f359773ca782a74a8d1377453594eaa84fec0a7c6ed0673c8fb77172bdcd02206f09a9b7f5fed3deb5950c4efb28143b1d015c842e458a6e8d996bbba5508a70[ALL|FORKID] 02b26df59c140c6d5211e0814f91a6e8a66c887a6c9034b47d219ebfadd62b0d67",
                    "hex": "483045022100dd59f359773ca782a74a8d1377453594eaa84fec0a7c6ed0673c8fb77172bdcd02206f09a9b7f5fed3deb5950c4efb28143b1d015c842e458a6e8d996bbba5508a70412102b26df59c140c6d5211e0814f91a6e8a66c887a6c9034b47d219ebfadd62b0d67",
                },
                "sequence": 4294967294,
            }
        ],
        "vout": [
            {
                "value": 1.0,
                "n": 0,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 e6f014771208becd3fbb6bb997c99fede541cdac OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a914e6f014771208becd3fbb6bb997c99fede541cdac88ac",
                    "reqSigs": 1,
                    "type": "pubkeyhash",
                    "addresses": ["bchreg:qrn0q9rhzgytanflhd4mn97fnlk72swd4srmnfy3qm"],
                },
            },
            {
                "value": 47.99999582,
                "n": 1,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 2e6bed71d348b7bbc64aafa27b53a82547e3d57a OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a9142e6bed71d348b7bbc64aafa27b53a82547e3d57a88ac",
                    "reqSigs": 1,
                    "type": "pubkeyhash",
                    "addresses": ["bchreg:qqhxhmt36dyt0w7xf2h6y76n4qj50c740gpu8l9r3c"],
                },
            },
        ],
        "blockhash": "6767aa4c358797d580869c6ec8cd6e7005599aba1cd81863f3a01b52adb36a37",
        "confirmations": 6,
        "time": 1615793749,
        "blocktime": 1615793749,
        "hex": "010000000177016748df5293205e28267d1cb0b256b2564595279d51e17667b0d64b93a354010000006b483045022100dd59f359773ca782a74a8d1377453594eaa84fec0a7c6ed0673c8fb77172bdcd02206f09a9b7f5fed3deb5950c4efb28143b1d015c842e458a6e8d996bbba5508a70412102b26df59c140c6d5211e0814f91a6e8a66c887a6c9034b47d219ebfadd62b0d67feffffff0200e1f505000000001976a914e6f014771208becd3fbb6bb997c99fede541cdac88ac5e2e1a1e010000001976a9142e6bed71d348b7bbc64aafa27b53a82547e3d57a88acdf000000",
    },
    "error": None,
    "id": 0,
}


address_details = {
    "addrStr": "mofnoitUXBfNFLKqwwomj5KwBVqJeydSyx",
    "balanceSat": 100000000,
    "unconfirmedBalanceSat": 100000000,
    "balance": 1.0,
    "unconfirmedBalance": 1.0,
    "transactions": [
        "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce"
    ],
    "txApperances": 1,
    "unconfirmedTxApperances": 1,
    "totalReceived": 1.0,
    "totalReceivedSat": 100000000,
    "totalSent": 0.0,
    "totalSentSat": 0,
}

address_utxo = [
    {
        "height": 0,
        "tx_hash": "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce",
        "tx_pos": 0,
        "value": 100000000,
    }
]

address_tx = {
    "blockhash": "0000000000000000000000000000000000000000000000000000000000000000",
    "blocktime": 0,
    "confirmations": 0,
    "hash": "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce",
    "height": 0,
    "hex": "01000000014821fd605a2fa96c786e994648811beea888f4338a09b2b0dc2cc3eac1e73400010000006a47304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24412102498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260feffffff0200e1f505000000001976a914596cd4508cd763b019bd4b83e1b4ca0fa58281a688ac7c4c2418010000001976a91415b3fba239bc86328d55507cfff76b1447de710c88ace5000000",
    "locktime": 229,
    "size": 225,
    "time": 0,
    "txid": "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce",
    "vin": [
        {
            "scriptSig": "47304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24412102498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260",
            "sequence": 4294967294,
            "txid": "0034e7c1eac32cdcb0b2098a33f488a8ee1b814846996e786ca92f5a60fd2148",
            "vout": 1,
        }
    ],
    "vout": [
        {
            "scriptPubKey": "76a914596cd4508cd763b019bd4b83e1b4ca0fa58281a688ac",
            "value": 100000000,
        },
        {
            "scriptPubKey": "76a91415b3fba239bc86328d55507cfff76b1447de710c88ac",
            "value": 4699999356,
        },
    ],
}

address_result = [
    {
        "height": 0,
        "txid": "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce",
        "vout": 0,
        "satoshis": 100000000,
        "amount": 1.0,
        "address": "mofnoitUXBfNFLKqwwomj5KwBVqJeydSyx",
        "scriptPubKey": "76a914596cd4508cd763b019bd4b83e1b4ca0fa58281a688ac",
        "confirmations": 0,
    }
]

transaction_call_method_1 = {
    "txid": "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce",
    "size": 225,
    "version": 1,
    "locktime": 229,
    "vin": [
        {
            "txid": "0034e7c1eac32cdcb0b2098a33f488a8ee1b814846996e786ca92f5a60fd2148",
            "vout": 1,
            "scriptSig": {
                "asm": "304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24[ALL|FORKID] 02498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260",
                "hex": "47304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24412102498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260",
            },
            "sequence": 4294967294,
        }
    ],
    "vout": [
        {
            "value": 1.0,
            "n": 0,
            "scriptPubKey": {
                "asm": "OP_DUP OP_HASH160 596cd4508cd763b019bd4b83e1b4ca0fa58281a6 OP_EQUALVERIFY OP_CHECKSIG",
                "hex": "76a914596cd4508cd763b019bd4b83e1b4ca0fa58281a688ac",
                "reqSigs": 1,
                "type": "pubkeyhash",
                "addresses": ["bchreg:qpvke4zs3ntk8vqeh49c8cd5eg86tq5p5cxqce75q9"],
            },
        },
        {
            "value": 46.99999356,
            "n": 1,
            "scriptPubKey": {
                "asm": "OP_DUP OP_HASH160 15b3fba239bc86328d55507cfff76b1447de710c OP_EQUALVERIFY OP_CHECKSIG",
                "hex": "76a91415b3fba239bc86328d55507cfff76b1447de710c88ac",
                "reqSigs": 1,
                "type": "pubkeyhash",
                "addresses": ["bchreg:qq2m87az8x7gvv5d24g8ellhdv2y0hn3psamm0pptx"],
            },
        },
    ],
    "confirmations": 0,
    "time": 1615799934,
    "hex": "01000000014821fd605a2fa96c786e994648811beea888f4338a09b2b0dc2cc3eac1e73400010000006a47304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24412102498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260feffffff0200e1f505000000001976a914596cd4508cd763b019bd4b83e1b4ca0fa58281a688ac7c4c2418010000001976a91415b3fba239bc86328d55507cfff76b1447de710c88ace5000000",
}

transaction_call_method_tx = {
    "txid": "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce",
    "size": 225,
    "version": 1,
    "locktime": 229,
    "vin": [
        {
            "txid": "0034e7c1eac32cdcb0b2098a33f488a8ee1b814846996e786ca92f5a60fd2148",
            "vout": 1,
            "scriptSig": {
                "asm": "304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24[ALL|FORKID] 02498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260",
                "hex": "47304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24412102498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260",
            },
            "sequence": 4294967294,
        }
    ],
    "vout": [
        {
            "value": 1.0,
            "n": 0,
            "scriptPubKey": {
                "asm": "OP_DUP OP_HASH160 596cd4508cd763b019bd4b83e1b4ca0fa58281a6 OP_EQUALVERIFY OP_CHECKSIG",
                "hex": "76a914596cd4508cd763b019bd4b83e1b4ca0fa58281a688ac",
                "reqSigs": 1,
                "type": "pubkeyhash",
                "addresses": ["bchreg:qpvke4zs3ntk8vqeh49c8cd5eg86tq5p5cxqce75q9"],
            },
        },
        {
            "value": 46.99999356,
            "n": 1,
            "scriptPubKey": {
                "asm": "OP_DUP OP_HASH160 15b3fba239bc86328d55507cfff76b1447de710c OP_EQUALVERIFY OP_CHECKSIG",
                "hex": "76a91415b3fba239bc86328d55507cfff76b1447de710c88ac",
                "reqSigs": 1,
                "type": "pubkeyhash",
                "addresses": ["bchreg:qq2m87az8x7gvv5d24g8ellhdv2y0hn3psamm0pptx"],
            },
        },
    ],
    "confirmations": 0,
    "time": 1615799934,
    "hex": "01000000014821fd605a2fa96c786e994648811beea888f4338a09b2b0dc2cc3eac1e73400010000006a47304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24412102498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260feffffff0200e1f505000000001976a914596cd4508cd763b019bd4b83e1b4ca0fa58281a688ac7c4c2418010000001976a91415b3fba239bc86328d55507cfff76b1447de710c88ace5000000",
}

transaction_call_method_2 = {
    "txid": "0034e7c1eac32cdcb0b2098a33f488a8ee1b814846996e786ca92f5a60fd2148",
    "size": 226,
    "version": 1,
    "locktime": 223,
    "vin": [
        {
            "txid": "54a3934bd6b06776e1519d27954556b256b2b01c7d26285e209352df48670177",
            "vout": 1,
            "scriptSig": {
                "asm": "3045022100dd59f359773ca782a74a8d1377453594eaa84fec0a7c6ed0673c8fb77172bdcd02206f09a9b7f5fed3deb5950c4efb28143b1d015c842e458a6e8d996bbba5508a70[ALL|FORKID] 02b26df59c140c6d5211e0814f91a6e8a66c887a6c9034b47d219ebfadd62b0d67",
                "hex": "483045022100dd59f359773ca782a74a8d1377453594eaa84fec0a7c6ed0673c8fb77172bdcd02206f09a9b7f5fed3deb5950c4efb28143b1d015c842e458a6e8d996bbba5508a70412102b26df59c140c6d5211e0814f91a6e8a66c887a6c9034b47d219ebfadd62b0d67",
            },
            "sequence": 4294967294,
        }
    ],
    "vout": [
        {
            "value": 1.0,
            "n": 0,
            "scriptPubKey": {
                "asm": "OP_DUP OP_HASH160 e6f014771208becd3fbb6bb997c99fede541cdac OP_EQUALVERIFY OP_CHECKSIG",
                "hex": "76a914e6f014771208becd3fbb6bb997c99fede541cdac88ac",
                "reqSigs": 1,
                "type": "pubkeyhash",
                "addresses": ["bchreg:qrn0q9rhzgytanflhd4mn97fnlk72swd4srmnfy3qm"],
            },
        },
        {
            "value": 47.99999582,
            "n": 1,
            "scriptPubKey": {
                "asm": "OP_DUP OP_HASH160 2e6bed71d348b7bbc64aafa27b53a82547e3d57a OP_EQUALVERIFY OP_CHECKSIG",
                "hex": "76a9142e6bed71d348b7bbc64aafa27b53a82547e3d57a88ac",
                "reqSigs": 1,
                "type": "pubkeyhash",
                "addresses": ["bchreg:qqhxhmt36dyt0w7xf2h6y76n4qj50c740gpu8l9r3c"],
            },
        },
    ],
    "blockhash": "6767aa4c358797d580869c6ec8cd6e7005599aba1cd81863f3a01b52adb36a37",
    "confirmations": 6,
    "time": 1615793749,
    "blocktime": 1615793749,
    "hex": "010000000177016748df5293205e28267d1cb0b256b2564595279d51e17667b0d64b93a354010000006b483045022100dd59f359773ca782a74a8d1377453594eaa84fec0a7c6ed0673c8fb77172bdcd02206f09a9b7f5fed3deb5950c4efb28143b1d015c842e458a6e8d996bbba5508a70412102b26df59c140c6d5211e0814f91a6e8a66c887a6c9034b47d219ebfadd62b0d67feffffff0200e1f505000000001976a914e6f014771208becd3fbb6bb997c99fede541cdac88ac5e2e1a1e010000001976a9142e6bed71d348b7bbc64aafa27b53a82547e3d57a88acdf000000",
}

transaction_tx = {
    "txid": "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce",
    "size": 225,
    "version": 1,
    "locktime": 229,
    "vin": [
        {
            "txid": "0034e7c1eac32cdcb0b2098a33f488a8ee1b814846996e786ca92f5a60fd2148",
            "vout": 1,
            "scriptSig": {
                "asm": "304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24[ALL|FORKID] 02498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260",
                "hex": "47304402202e746040d0a99e662dee4d94b2b9096ded7bf06a62c19b910faa93ec71e28f290220237f89f9051a7009545e7526bf34efe3ba5d597d874d45f8fbfecfb923883f24412102498122094f5f4ea52d85cf5615e58e568247e4e5cdea46299b80724696009260",
            },
            "sequence": 4294967294,
            "value": 46.99999356,
            "n": 0,
            "doubleSpentTxID": None,
        }
    ],
    "vout": [
        {
            "value": 1.0,
            "n": 0,
            "scriptPubKey": {
                "asm": "OP_DUP OP_HASH160 596cd4508cd763b019bd4b83e1b4ca0fa58281a6 OP_EQUALVERIFY OP_CHECKSIG",
                "hex": "76a914596cd4508cd763b019bd4b83e1b4ca0fa58281a688ac",
                "reqSigs": 1,
                "type": "pubkeyhash",
                "addresses": ["bchreg:qpvke4zs3ntk8vqeh49c8cd5eg86tq5p5cxqce75q9"],
            },
            "spentTxId": None,
            "spentIndex": None,
            "spentHeight": None,
        },
        {
            "value": 46.99999356,
            "n": 1,
            "scriptPubKey": {
                "asm": "OP_DUP OP_HASH160 15b3fba239bc86328d55507cfff76b1447de710c OP_EQUALVERIFY OP_CHECKSIG",
                "hex": "76a91415b3fba239bc86328d55507cfff76b1447de710c88ac",
                "reqSigs": 1,
                "type": "pubkeyhash",
                "addresses": ["bchreg:qq2m87az8x7gvv5d24g8ellhdv2y0hn3psamm0pptx"],
            },
            "spentTxId": None,
            "spentIndex": None,
            "spentHeight": None,
        },
    ],
    "confirmations": 0,
    "time": 1615799934,
    "valueIn": 46.99999356,
    "valueOut": 47.99999356,
    "fees": -1.0,
}


block_hash_call_method_node = {
    "hash": "0c4339894f7aadb14884c259fbb177b6bea5a063b1c52d537aa7d0bd378827cf",
    "confirmations": 1,
    "size": 1120,
    "height": 229,
    "version": 536870912,
    "versionHex": "20000000",
    "merkleroot": "021b710f710a005be8f18a1947c3cc77a662eea2e0c444e8d8c4cc717ce925b9",
    "tx": [
        "10ab83efc33090427dd854d26027abd12e494e4815cf59ead96520e029d40c3b",
        "032cb0d26bfefa5c6e270f09b5fea38aa8cad65ec5f350b3e537d3766038d105",
        "29762bd1581e70d02655f9ada8f71a08a1d6f17f7c0af3fb5009686e3219533e",
    ],
    "time": 1615793957,
    "mediantime": 1615793749,
    "nonce": 1,
    "bits": "207fffff",
    "difficulty": 4.656542373906925e-10,
    "chainwork": "00000000000000000000000000000000000000000000000000000000000001cc",
    "previousblockhash": "55ea7e06280023e6e3fe65a8241664112f181b97295ab09a42f2bcef9e19ad46",
}

block_hash_electrum_result = {
    "blockhash": "0c4339894f7aadb14884c259fbb177b6bea5a063b1c52d537aa7d0bd378827cf",
    "blocktime": 1615793957,
    "confirmations": 0,
    "hash": "10ab83efc33090427dd854d26027abd12e494e4815cf59ead96520e029d40c3b",
    "height": 229,
    "hex": "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff1002e500510b2f454233322f414431322fffffffff013cfa052a01000000232103f469f84fb57096dbb5bf63b20c8c39503d584dad915a1fe35971cceb42759486ac00000000",
    "locktime": 0,
    "size": 111,
    "time": 1615793957,
    "txid": "10ab83efc33090427dd854d26027abd12e494e4815cf59ead96520e029d40c3b",
    "vin": [
        {
            "scriptSig": "02e500510b2f454233322f414431322f",
            "sequence": 4294967295,
            "txid": "0000000000000000000000000000000000000000000000000000000000000000",
            "vout": 4294967295,
        }
    ],
    "vout": [
        {
            "scriptPubKey": "2103f469f84fb57096dbb5bf63b20c8c39503d584dad915a1fe35971cceb42759486ac",
            "value": 5000002108,
        }
    ],
}

block_hash_result = {
    "hash": "0c4339894f7aadb14884c259fbb177b6bea5a063b1c52d537aa7d0bd378827cf",
    "confirmations": 1,
    "size": 1120,
    "height": 229,
    "version": 536870912,
    "versionHex": "20000000",
    "merkleroot": "021b710f710a005be8f18a1947c3cc77a662eea2e0c444e8d8c4cc717ce925b9",
    "tx": [
        "10ab83efc33090427dd854d26027abd12e494e4815cf59ead96520e029d40c3b",
        "032cb0d26bfefa5c6e270f09b5fea38aa8cad65ec5f350b3e537d3766038d105",
        "29762bd1581e70d02655f9ada8f71a08a1d6f17f7c0af3fb5009686e3219533e",
    ],
    "time": 1615793957,
    "mediantime": 1615793749,
    "nonce": 1,
    "bits": "207fffff",
    "difficulty": 4.656542373906925e-10,
    "chainwork": "00000000000000000000000000000000000000000000000000000000000001cc",
    "previousblockhash": "55ea7e06280023e6e3fe65a8241664112f181b97295ab09a42f2bcef9e19ad46",
    "isMainChain": True,
    "poolInfo": {},
    "reward": 50.00002108,
}
result: {
    "hash": "0c4339894f7aadb14884c259fbb177b6bea5a063b1c52d537aa7d0bd378827cf",
    "confirmations": 1,
    "size": 1120,
    "height": 229,
    "version": 536870912,
    "versionHex": "20000000",
    "merkleroot": "021b710f710a005be8f18a1947c3cc77a662eea2e0c444e8d8c4cc717ce925b9",
    "tx": [
        "10ab83efc33090427dd854d26027abd12e494e4815cf59ead96520e029d40c3b",
        "032cb0d26bfefa5c6e270f09b5fea38aa8cad65ec5f350b3e537d3766038d105",
        "29762bd1581e70d02655f9ada8f71a08a1d6f17f7c0af3fb5009686e3219533e",
    ],
    "time": 1615793957,
    "mediantime": 1615793749,
    "nonce": 1,
    "bits": "207fffff",
    "difficulty": 4.656542373906925e-10,
    "chainwork": "00000000000000000000000000000000000000000000000000000000000001cc",
    "previousblockhash": "55ea7e06280023e6e3fe65a8241664112f181b97295ab09a42f2bcef9e19ad46",
    "isMainChain": True,
    "poolInfo": {},
    "reward": 50.00002108,
}

mocked_post_txid1 = "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce"

mocked_post_txid2 = "0034e7c1eac32cdcb0b2098a33f488a8ee1b814846996e786ca92f5a60fd2148"

get_block_details_blockhash = "0c4339894f7aadb14884c259fbb177b6bea5a063b1c52d537aa7d0bd378827cf"

get_transaction_details_tx = "13f46c6c25a22d8dbac9e01f0d8d4e2f68d37214eb282362f2e48be12d8b53ce"
