import sys
import WebServer

HOST, PORT = '', 8080


def make_server(server_address, app_handler):
    web_server = WebServer.WebServer(server_address)
    web_server.set_app_handler(app_handler)
    return web_server


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module_name, handler_name = app_path.split(':')
    module = __import__(module_name)
    handler = getattr(module, handler_name)
    server = make_server((HOST, PORT), handler)
    print('WebServer: Serving HTTP on port {0} ...\n'.format(PORT))
    server.serve_forever()
