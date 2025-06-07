import http.server, ssl, os

os.chdir("mirror-data")  # Folder to hold delivered files

server_address = ('127.0.0.1', 4444)  # Test: 4444, Prod: 4445
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket(httpd.socket,
    server_side=True,
    certfile="C:/Users/sarit/OneDrive/Desktop/my-product-project/certs/test.crt",
    keyfile="C:/Users/sarit/OneDrive/Desktop/my-product-project/certs/test.key",
    ssl_version=ssl.PROTOCOL_TLS)

print("Prod Mirror server running at https://127.0.0.1:4444")
httpd.serve_forever()
