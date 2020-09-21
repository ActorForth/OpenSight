#!/usr/bin/env python3

# This is an open source implementation of the Insight service to use with the 
# rest.bitcoin.com API

import json
import logging
from sys import argv
from http.server import BaseHTTPRequestHandler, HTTPServer

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        # the hardcoded value to send to Rest.bitcoin.com
        # Send header response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()

        # the hardcoded value to send to Rest.bitcoin.com
        # String should use triple quotes to avoid Python escaping single quotes
        hardcoded_response = """
        {
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
        """

        # Send hardcoded response back to rest.bitcoin.com, must be encoded byte array
        self.wfile.write(bytes(hardcoded_response.encode("utf-8")))
        self.wfile.close()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=3001):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

