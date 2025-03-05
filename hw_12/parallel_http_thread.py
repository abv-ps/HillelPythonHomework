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
- main: The main function that starts the server and sends multiple requests
  concurrently using threads.

Usage:
    The module starts an HTTP server that listens on `0.0.0.0` and port `8080` by default.
    Multiple threads are created to send GET requests to the server, and the responses are printed.
    To stop the server, use Ctrl+C in the terminal.
"""
import logging
import time
import threading
import http.server
from typing import Tuple
import requests
from log_wrapper import log_wrapper

logging.basicConfig(
    filename='server_requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@log_wrapper
class ThreadedHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler that serves responses to multiple clients using threads.

    This class extends the `SimpleHTTPRequestHandler` to allow handling multiple
    HTTP requests concurrently using threads. It overrides the `do_GET` method
    to return a custom response for GET requests.

    Inherits from:
        http.server.SimpleHTTPRequestHandler

    Methods:
        do_GET(self) -> None
            Handles GET requests and responds with a simple text message.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._status_code = None
        self._response_body = None

    def do_GET(self) -> None:
        """
    Handles GET requests and sends a simple response to the client.

    This method overrides the default `do_GET` behavior from the `SimpleHTTPRequestHandler`.
    It sends an HTTP 200 status code, sets the `Content-Type` header to `text/plain`,
    and returns a simple message "Hello! This is a multithreaded HTTP server."

    Parameters:
        self (ThreadedHTTPRequestHandler): The instance of the handler processing the request.

    Response:
        - HTTP status code 200 (OK).
        - Content-Type header: text/plain.
        - Response body: "Hello! This is a multithreaded HTTP server."
    """
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        message = "Hello! This is a multithreaded HTTP server."
        self.wfile.write(message.encode())

        self._status_code = 200
        self._response_body = message


def run_server(host: str = "127.0.0.1", port: int = 7777) -> None:
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
        response = requests.get("http://127.0.0.1:7777", timeout=5)
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


def main() -> None:
    """
    Starts the HTTP server and sends multiple concurrent requests using threads.

    This function performs the following steps:
        1. Starts the server in a separate daemon thread.
        2. Waits for 0.5 seconds to allow the server to start.
        3. Creates 5 threads that concurrently send HTTP GET requests to the server.
        4. Waits for all request threads to finish.

    The server runs in the background, and multiple requests are sent simultaneously to
    test the server's ability to handle concurrent connections.

    Args:
        None

    Returns:
        None
    """
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    time.sleep(0.5)

    threads = [threading.Thread(target=send_request) for _ in range(5)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
