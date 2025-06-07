import http.server
import ssl
import os
import webbrowser  # <-- Add this import

PORT = 4444

# Change directory to serve artifacts
os.chdir('dev/build')

server_address = ('127.0.0.1', PORT)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='../../certs/staging.crt', keyfile='../../certs/staging.key')

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

# Open in default browser automatically
webbrowser.open(f'https://127.0.0.1:{PORT}')

print(f"Staging server running at https://127.0.0.1:{PORT}")
httpd.serve_forever()
