# app.py - a minimal flask api using flask_restful
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

class EntryPoint(Resource):
    def get(self):
        return {'hello': 'world'}


class AddressDetail(Resource):
    def get(self, address):
        args = parser.parse_args()

        return {
            "balance": 0.00014673,
            "balanceSat": 14673,
            "totalReceived": 0.10200541,
            "totalReceivedSat": 10200541,
            "totalSent": 0.10185868,
            "totalSentSat": 10185868,
            "unconfirmedBalance": 0,
            "unconfirmedBalanceSat": 0,
            "unconfirmedTxApperances": 0,
            "txApperances": 44,
            "transactions": [
                "78ffb00ae72702b0a37f7c2e85cc40caca7fde3086637f18d29e4a208e2bbfb5",
                "d5228d2cdc77fbe5a9aa79f19b0933b6802f9f0067f42847fc4fe343664723e5",
                "5cfb7ea6c23ec8b2b98a0bcd5d204b5432b868c5d8165dce48aaeaf6b5267176",
                "d31dc2cf66fe4d3d3ae18e1065def58a64920746b1702b52f060e5edeea9883b",
                "41e9a118765ecf7a1ba4487c0863e23dba343cc5880381a72f0365ac2546c5fa",
                "2f902dec880568511cefa87b9dd761563edeba9c8ba784dc9fca2f7c8c4e6f97",
                "eea57285462dd70dadcd431fc814857b3f81fe4d0a059a8c02c12fd7d33c02d1",
                "282b3b296b6aed7122586ed69f7a57d35584eaf94a4d1b1ad7d1b05d36cb79d1",
                "ac444896b3e32d17824fa6573eed3b89768c5c9085b7a71f3ba88e9d5ba67355",
                "a5f972572ee1753e2fd2457dd61ce5f40fa2f8a30173d417e49feef7542c96a1",
                "5165dc531aad05d1149bb0f0d9b7bda99c73e2f05e314bcfb5b4bb9ca5e1af5e",
                "54edaa42ff3d6559884a84ebb9bf5ef255635902f5f23b4854245d6b093d41d4",
                "7a12ea2c83d0c8a5d0f643974b0f04bc19be185c9011ed8fc33255a61d3198bb",
                "2b0825188e909410a20a6fbdc58ff5ccf368844273f93f551222c91e6d0fa888",
                "bd6aeeb0748251bb5dba7252ac766fb208c9909d7663c099568225d3bc998a7f",
                "7898bb1a8c5d933f9c2b24270522e8705b897c2f8d5b1c3477a6b952f2fe22ae",
                "8d35668a6838de8faa8dff5d8dedeb114bd8ffe6ae73d926264bc8328b2c46b5",
                "741b4692a14088438ab142cf0865fcbf3977aa7dbd2aafa9bf5f45e75e5e199a",
                "15f6a584080b04911121fbaca7bfcf3dd64ef2bfa5a01daf31e05a296c3e5e9e",
                "376de807f63253584c3edb80f92832ea90e8fdd7d8e68b2602e230d1b015e311",
                "11205c557af139f382c43f1f09f223cf28c64d939951fd569e5a30eee6178ccd",
                "ae05a78086b8d64db26d3047de3d6959a68f2a1ed3017ddf927e2c3b20a80b31",
                "7e0fc3cac7504d45b0f2ce68e807e592f0edf17914ab618a4cb4d93403d11c98",
                "eb5d0902e4a303f38223ecebb06bbf14da8a07d1ebb2d77a89dfb9e00e286c10",
                "1cafaacdfb85b0c33f496bf2c03c4f2ede508479bbad56ae99164dfd823a823f",
                "788add6a5cd961bdf7ca6145a3112462e0e51523d84a4a48047407a795433947",
                "49f09b616824a05eb14ae50c9fbc5d6a0c414d66a7d0b217aa75340c00ed8b85",
                "00f075805adf2a34563ecca33071d660a4c1e91d7d7045282c54554ee4844739",
                "8d048fd00cf375ba9bbea43730da1ce86fc3cb4026e1dd0e751c07fa50a652c6",
                "ac0e82ea84f93444602a99199dd80793f79a8ece5ac86156d2fff34f0bad44b2",
                "342f6815845797e0748f4716c923a0dc9b87de649b69925b36422f6d2dc23b7f",
                "0839a16b2411a1220c64c4d32a4c9b1e77ac5f47558921cf7c0a2adf25e0eb41",
                "62f42995711cb0308dac4203c5deaa2985f120559131e66aebc5164426fb6cee",
                "e0aadd861a06993e39af932bb0b9ad69e7b37ef5843a13c6724789e1c94f3513",
                "2ada093fe13c9c04da9582bb304923ce08312eaec92560b9128cdb9e93c5f52f",
                "925490ce60334aca204d82a61b634d89fe4cc9de429c7b6cb5ec420df3e3be5e",
                "60cb69f29c150378abe21d157858713f82c4e2122867597a2573474763a9e94e",
                "369a589173969c1c882cfb2d82b1e0ec90076ec827ff9d0f32ffc115690c93c3",
                "43324ef3f5fdd55b645ba14de8c0667be9b223d60b3d1dcd76cf8fdeb0fd32e4",
                "d2985c9b1c5c18fc2f6a963b7cb850606c4a18fcb85619057211ce3c8bcec696",
                "2dc053f55a666a3d2a08b1c680b704d62a55506d14ad884add87edcc56b9277d",
                "dded59fe377517e52918deae8912a096658ebf5ae61992d39953c8bc3932a11b",
                "544c15ce35c0f2e808d28f29d6587f1ec9276233e29856b7f2938cf0daef0026",
                "81039b1d7b855b133f359f9dc65f776bd105650153a941675fedc504228ddbd3"
            ],
            "addrStr": "bchreg:qp7j7jy8c0q0n70cs4mpks3mcqu5perw6gmz4zu4xc"
        }


class TransactionDetail(Resource):
    def get(self, transaction):
        args = parser.parse_args()

        return {
            "txid": "40112ab9d2b5f98427839272d7a1e23dd2afc6c8355626f373e076c2ab5c2f72",
            "version": 1,
            "locktime": 0,
            "vin": [
                {
                    "txid": "56a081af7f5162b0ddcf5f629c7867a072b785df9146576b1d39f30f3f8d4af9",
                    "vout": 1,
                    "sequence": 4294967295,
                    "n": 0,
                    "scriptSig": {
                        "hex": "473044022065d3d111db75d01d001bbd411961759f7b2eacab379912c159208f8147e322ea02201fe597474710966b16ae97b0e0673d5ca66bfe8618f89addea833f6e87cf4e3641210289d92b4239c112e97db3aac9590681968bd00415e974dba04bc81cca96b8c7ec",
                        "asm": "3044022065d3d111db75d01d001bbd411961759f7b2eacab379912c159208f8147e322ea02201fe597474710966b16ae97b0e0673d5ca66bfe8618f89addea833f6e87cf4e36[ALL|FORKID] 0289d92b4239c112e97db3aac9590681968bd00415e974dba04bc81cca96b8c7ec"
                    },
                    "valueSat": 528122066,
                }
            ],
            "vout": [
                {
                    "value": "0.00002000",
                    "n": 0,
                    "scriptPubKey": {
                        "hex": "76a91432b57f34861bcbe33a701be9ac3a50288fbc0a3d88ac",
                        "asm": "OP_DUP OP_HASH160 32b57f34861bcbe33a701be9ac3a50288fbc0a3d OP_EQUALVERIFY OP_CHECKSIG",
                        "addresses": [
                            "mk95WGfZS9Tuk7o8acBwiuDyhtVhUACMaZ"
                        ],
                        "type": "pubkeyhash",
                    },
                    "spentTxId": None,
                    "spentIndex": None,
                    "spentHeight": None
                },
                {
                    "value": "5.28119752",
                    "n": 1,
                    "scriptPubKey": {
                        "hex": "76a914b8e0a1c9040f8636a453ba077d7fa5f2318c7d0c88ac",
                        "asm": "OP_DUP OP_HASH160 b8e0a1c9040f8636a453ba077d7fa5f2318c7d0c OP_EQUALVERIFY OP_CHECKSIG",
                        "addresses": [
                            "mxNVj45miWLQyG8DwjX2YsPLoTUK7raHuy"
                        ],
                        "type": "pubkeyhash",
                    },
                    "spentTxId": "fd6bd179c769a044d93710996dbf4dc33fa4cf9eb3e408d73880b74254d184c6",
                    "spentIndex": 0,
                    "spentHeight": 1274549
                }
            ],
            "blockhash": "00000000002a7077295ec8d4f7afdace8d37d694384cc821e406834fe57aeaae",
            "blockheight": 1274549,
            "confirmations": 103912,
            "time": 1545086356,
            "blocktime": 1545086356,
            "valueOut": 5.28121752,
            "size": 225,
            "valueIn": 5.28122066,
            "fees": 0.00000314
        }


class Transactions(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('address', type=str)
        parser.add_argument('pageNum', type=str)

        args = parser.parse_args()

        return {
            "pagesTotal": 11844,
            "txs": [
                {
                    "txid": "f0a4bea799ae42ab5ea597ca5a768c44efbee70e71d51bca304f54a30161f747",
                    "version": 1,
                    "locktime": 0,
                    "vin": [
                        {
                            "txid": "c788ace35c42b70cf5abe5d085cf1f4cc621642e0a0a5f8474935573ef725ac3",
                            "vout": 1,
                            "sequence": 4294967295,
                            "n": 0,
                            "scriptSig": {
                                "hex": "473044022045fd1fdbfb516d67ca68ef4b33260b7cd90ae04c81adaab638ce065c81d21c2d022064af3f1847e512c5e62b138bf8f9fdbe98738744ec51bf1946c5d3bcf479c50a41210289d92b4239c112e97db3aac9590681968bd00415e974dba04bc81cca96b8c7ec",
                                "asm": "3044022045fd1fdbfb516d67ca68ef4b33260b7cd90ae04c81adaab638ce065c81d21c2d022064af3f1847e512c5e62b138bf8f9fdbe98738744ec51bf1946c5d3bcf479c50a[ALL|FORKID] 0289d92b4239c112e97db3aac9590681968bd00415e974dba04bc81cca96b8c7ec"
                            },
                            "addr": "mxNVj45miWLQyG8DwjX2YsPLoTUK7raHuy",
                            "valueSat": 261777652,
                            "value": 2.61777652,
                            "doubleSpentTxID": None
                        }
                    ],
                    "vout": [
                        {
                            "value": "0.00002000",
                            "n": 0,
                            "scriptPubKey": {
                                "hex": "76a91432b57f34861bcbe33a701be9ac3a50288fbc0a3d88ac",
                                "asm": "OP_DUP OP_HASH160 32b57f34861bcbe33a701be9ac3a50288fbc0a3d OP_EQUALVERIFY OP_CHECKSIG",
                                "addresses": [
                                    "mk95WGfZS9Tuk7o8acBwiuDyhtVhUACMaZ"
                                ],
                                "type": "pubkeyhash"
                            },
                            "spentTxId": None,
                            "spentIndex": None,
                            "spentHeight": None
                        },
                        {
                            "value": "2.61775317",
                            "n": 1,
                            "scriptPubKey": {
                                "hex": "76a914b8e0a1c9040f8636a453ba077d7fa5f2318c7d0c88ac",
                                "asm": "OP_DUP OP_HASH160 b8e0a1c9040f8636a453ba077d7fa5f2318c7d0c OP_EQUALVERIFY OP_CHECKSIG",
                                "addresses": [
                                    "mxNVj45miWLQyG8DwjX2YsPLoTUK7raHuy"
                                ],
                                "type": "pubkeyhash"
                            },
                            "spentTxId": "d14aaf9aa0c8bf8f987f91e1565626529416866b25fbe3eb0b0540c4700df185",
                            "spentIndex": 0,
                            "spentHeight": 1292555
                        }
                    ],
                    "blockhash": "000000004c4b9e84d45d986aec26783a270a992bfcc226143d3f2646ecdab374",
                    "blockheight": 1292555,
                    "confirmations": 85906,
                    "time": 1552511340,
                    "blocktime": 1552511340,
                    "valueOut": 2.61777317,
                    "size": 225,
                    "valueIn": 2.61777652,
                    "fees": 0.00000335
                },
            ],
            "legacyAddress": "mxNVj45miWLQyG8DwjX2YsPLoTUK7raHuy",
            "cashAddress": "bchtest:qzuwpgwfqs8cvd4y2waqwltl5herrrrapsujlsdcwf",
            "currentPage": 0
        }


class AddressUtxos(Resource):
    def get(self, address):

        return [
            {
                "txid": "cb59443f4ca390df41e66db619cd385bac03a8271ec820bb7e8bab41a6cbcfea",
                "vout": 0,
                "amount": 1.56261,
                "satoshis": 156261000,
                "height": 1255647,
                "confirmations": 122814,
                "address": "a34bd369e9dca0837d5480fd7c3e6cd9449ac154",
                "scriptPubKey": "76a914a34bd369e9dca0837d5480fd7c3e6cd9449ac15488ac"
            },
            {
                "txid": "5bbea2c8507b2a2e3482c3a76536f12112577e47a6b386678458a0949639d03b",
                "vout": 0,
                "amount": 1.563855,
                "satoshis": 156385500,
                "height": 1255646,
                "confirmations": 122815,
                "address": "a34bd369e9dca0837d5480fd7c3e6cd9449ac154",
                "scriptPubKey": "76a914a34bd369e9dca0837d5480fd7c3e6cd9449ac15488ac"
            },
            {
                "txid": "ef78817602661ff4f52d6ab959aa557b4b2d67fd12c4db879fe62175aa18b327",
                "vout": 0,
                "amount": 1.5645668,
                "satoshis": 156456680,
                "height": 1255644,
                "confirmations": 122817,
                "address": "a34bd369e9dca0837d5480fd7c3e6cd9449ac154",
                "scriptPubKey": "76a914a34bd369e9dca0837d5480fd7c3e6cd9449ac15488ac"
            }
        ]


class BlockDetails(Resource):
    def get(self, blockhash):

        return {
            "hash": "3c91710d77bcf716f3932576f7403e6274ac0510f0336cc779bb3d04d473a857",
            "confirmations": 161,
            "size": 192,
            "height": 250,
            "version": 536870912,
            "versionHex": "20000000",
            "merkleroot": "22751eb4381b31ef4c27f0bff8aa98bd1d87b4f6c6ee9cabcf12ee914d6bf124",
            "tx": [
                "22751eb4381b31ef4c27f0bff8aa98bd1d87b4f6c6ee9cabcf12ee914d6bf124"
            ],
            "time": 1600244549,
            "mediantime": 1600244548,
            "nonce": 0,
            "bits": "207fffff",
            "difficulty": 4.656542373906925e-10,
            "chainwork": "00000000000000000000000000000000000000000000000000000000000001f6",
            "previousblockhash": "2b7fdfe28d9b28d094c8866d3e781022969e8bee93d0f364a7af01fed77b3c71",
            "nextblockhash": "1e7a7e60154bc72d291247958c0fcd3b786516abd4c4463c1ddc1cf23db35d1d"
        }



api.add_resource(EntryPoint, '/')
api.add_resource(AddressDetail, '/api/addr/<address>')
api.add_resource(TransactionDetail, '/api/tx/<transaction>')
api.add_resource(Transactions, '/api/txs/')
api.add_resource(AddressUtxos, '/api/addr/<address>/utxo')
api.add_resource(BlockDetails, '/api/block/<blockhash>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='3001')
