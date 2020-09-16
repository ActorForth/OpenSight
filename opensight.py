#!/usr/bin/env python3

# This is an open source implementation of the Insight service to use with the 
# rest.bitcoin.com API

import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler

def return_addr():
    print("return address")

class OpenInsight(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/captureImage':
            return_addr()

        self.send_response(200)

httpd = SocketServer.TCPServer(("", 3001), OpenInsight)
httpd.serve_forever()

