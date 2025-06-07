import http.server
import ssl
import threading
import webbrowser
import time
import os

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Force directory listing even if index.html exists
        if self.path == "/":
            self.path = "/."
        return super().do_GET()

    def list_directory(self, path):
        try:
            file_list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        file_list.sort()
        displaypath = os.path.relpath(path)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Mirror Server - Directory Listing</title>
            <style>
                body {{
                    font-family: 'Segoe UI', sans-serif;
                    background: linear-gradient(to right, #e0f7fa, #fffde7);
                    padding: 40px;
                    color: #333;
                }}
                h1 {{
                    font-size: 2.5rem;
                    color: #00796B;
                }}
                ul {{
                    list-style-type: none;
                    padding: 0;
                }}
                li {{
                    margin: 10px 0;
                    font-size: 1.2rem;
                }}
                a {{
                    text-decoration: none;
                    color: #004d40;
                    font-weight: bold;
                }}
                a:hover {{
                    color: #00796B;
                }}
                .container {{
                    background: #ffffff;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📁 Directory listing for {displaypath}</h1>
                <ul>
        """

        for name in file_list:
            fullname = os.path.join(path, name)
            display_name = link_name = name
            if os.path.isdir(fullname):
                display_name += "/"
                link_name += "/"
            html += f'<li><a href="{link_name}">{display_name}</a></li>'

        html += """
                </ul>
            </div>
        </body>
        </html>
        """

        encoded = html.encode('utf-8', 'surrogateescape')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
        return None

def run_server():
    os.chdir(r'C:\Users\sarit\OneDrive\Desktop\my-product-project')
    print("Current directory:", os.getcwd())
    print("Files:", os.listdir('.'))

    server_address = ('127.0.0.1', 4443)
    httpd = http.server.HTTPServer(server_address, CustomHandler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='certs/mirror.crt', keyfile='certs/mirror.key')
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print("Mirror Server running at https://localhost:4443")
    httpd.serve_forever()

server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

time.sleep(1)
#webbrowser.open('https://127.0.0.1:4443/')
server_thread.join()
