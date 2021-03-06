#!/usr/bin/env python3
#
# Copyright (C) 2014 Blindspot Security LLC
# by Timothy D. Morgan
# twits: @ecbftw

import sys
import time
import socketserver
import http.server


class EchoHandler(http.server.BaseHTTPRequestHandler):
    """
    """

    def do_GET(self):
        #resolution = time.clock_getres(time.CLOCK_MONOTONIC)
        received = int(time.monotonic()*1000000000)
        wait_time = 0
        if 't=' in self.path:
            wait_time = int(self.path.split('t=', 1)[1], 10)

        # Use a busy-wait with monotonic clock.  More accurate than time.sleep()
        finish = received + wait_time
        now = int(time.monotonic()*1000000000)
        while now < finish:
            now = int(time.monotonic()*1000000000)
        
        self.send_response(200)
        self.send_header('Content-Type','text/plain; charset=UTF-8')
        self.end_headers()

        content = "waited: %d\n" % (now - received)
        self.wfile.write(content.encode('utf-8'))
        self.wfile.flush()


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 3240
    server = socketserver.TCPServer((HOST, PORT), EchoHandler)
    server.serve_forever()
