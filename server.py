#!/usr/bin/env python3
"""HTTP server with COOP/COEP headers required by MediaPipe WASM."""
import http.server
import socketserver
import os

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        # Also allow CDN resources
        self.send_header('Cross-Origin-Resource-Policy', 'cross-origin')
        super().end_headers()

    def log_message(self, format, *args):
        print("[%s] %s" % (self.log_date_time_string(), args[0]))

os.chdir(os.path.dirname(os.path.abspath(__file__)))
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server started: http://localhost:%d/index.html" % PORT)
    print("  (COOP/COEP headers enabled for WASM)")
    httpd.serve_forever()
