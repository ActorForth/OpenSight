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
        hardcoded_response = """{"hash": "789c69d284f0fdd25c11a109ff623720b4dab65f5b8c7b81711790df769f37c3", "confirmations": 1, "size": 192, "height": 410, "version": 536870912, "versionHex": "20000000", "merkleroot": "59069725aa2dde43015270f19fed9442aad2f4ff674b65605122e6acd22d8ba1", "tx": ["59069725aa2dde43015270f19fed9442aad2f4ff674b65605122e6acd22d8ba1"], "time": 1600244712, "mediantime": 1600244711, "nonce": 1, "bits": "207fffff", "difficulty": 4.656542373906925e-10, "chainwork": "0000000000000000000000000000000000000000000000000000000000000336", "previousblockhash": "055f7518a6551207cb23e735c1c9594c33e0d98ae84f07bcf907711b5e0c44b9"}"""

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

