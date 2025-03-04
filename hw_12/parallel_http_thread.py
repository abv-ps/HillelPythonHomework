"""
This module implements a multithreaded HTTP server that handles incoming GET requests
and responds with a simple message. It uses the `http.server` module to create the server
and the `threading` module to handle multiple requests concurrently.

The server is designed to run in a separate thread to allow for concurrent HTTP requests
sent by multiple client threads.

Key components:
- ThreadedHTTPRequestHandler: A custom handler that responds to HTTP GET requests.
- run_server: A function that starts the HTTP server.
- send_request: A function that sends an HTTP GET request to the server and prints the response.
- main: The main function that starts the server and sends multiple requests concurrently using threads.

Usage:
    The module starts an HTTP server that listens on `0.0.0.0` and port `8080` by default.
    Multiple threads are created to send GET requests to the server, and the responses are printed.
    To stop the server, use Ctrl+C in the terminal.
"""

import requests
import threading
import http.server
from typing import Tuple


class ThreadedHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler that serves responses to multiple clients using threads.
    """

    def do_GET(self) -> None:
        """
        Handles GET requests and responds with a simple message.
        """
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello! This is a multithreaded HTTP server.")


def run_server(host: str = "0.0.0.0", port: int = 8080) -> None:
    """
    Starts a threaded HTTP server.

    Args:
        host (str): The host address to bind the server to.
        port (int): The port number to listen on.
    """
    server_address: Tuple[str, int] = (host, port)
    httpd: http.server.ThreadingHTTPServer = http.server.ThreadingHTTPServer(
        server_address, ThreadedHTTPRequestHandler
    )
    print(f"Serving HTTP on {host} port {port} (Press Ctrl+C to stop)...")
    httpd.serve_forever()


def send_request() -> None:
    """
    Sends an HTTP GET request to the server and prints the response.

    Handles possible network errors.
    """
    try:
        response = requests.get("http://127.0.0.1:8080")
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


def main() -> None:
    """
    Starts the server and sends multiple requests concurrently using threads.
    """
    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Give the server some time to start up before sending requests
    import time
    time.sleep(0.5)

    # Start threads to send requests
    threads = [threading.Thread(target=send_request) for _ in range(5)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
