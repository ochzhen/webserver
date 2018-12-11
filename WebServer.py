import socket
import sys
import datetime
import io


def print_to_console(text, char='-'):
    print(''.join('{1} {0}\n'.format(line, char) for line in text.splitlines()))


class WebServer:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, server_address, backlog=10):
        self.request_backlog = backlog
        self._sock = socket.socket(self.address_family, self.socket_type)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(server_address)
        self._sock.listen(self.request_backlog)
        host, port = self._sock.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self._headers_set = []
        self._app_handler = None

    def set_app_handler(self, app_handler):
        self._app_handler = app_handler

    def serve_forever(self):
        while True:
            connection, address = self._sock.accept()
            self._handle_request(connection)

    def _handle_request(self, connection):
        request = connection.recv(1024).decode()
        print_to_console(request, '>')
        method, path, version = self._parse_request(request)
        env = self._get_environ(request, method, path)
        body = self._app_handler(env, self.start_response)
        response = self._build_response(body)
        print_to_console(response, '<')
        try:
            connection.sendall(response.encode())
        finally:
            connection.close()

    def _get_environ(self, request, method, path):
        env = {
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': io.StringIO(request),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'SERVER_NAME': self.server_name,
            'SERVER_PORT': str(self.server_port)
        }
        return env

    def start_response(self, status, response_headers):
        server_headers = [
            ('Date', datetime.datetime.utcnow()),
            ('Server', 'WebServer 1.0')
        ]
        self._headers_set = [status, server_headers + response_headers]

    def _build_response(self, body):
        status, headers = self._headers_set
        response = 'HTTP/1.1 {0}\r\n'.format(status) + \
                   ''.join('{0}: {1}\r\n'.format(*header) for header in headers) + \
                   '\r\n' + body
        return response

    @staticmethod
    def _parse_request(request):
        request_line = request.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        return request_line.split()
