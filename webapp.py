import routes


def app(environ, start_response):
    path = environ['PATH_INFO'].lower()
    method = environ['REQUEST_METHOD'].upper()
    status, body = process_request(path, method)
    headers = [('Content-Type', 'text/html')]
    start_response(status, headers)
    return body


def process_request(path, method):
    route_handler = find_route_handler(path, method)
    if not route_handler:
        return '404 NOT FOUND', routes.not_found()
    return '200 OK', route_handler()


def find_route_handler(path, method):
    if method != 'GET':
        return None
    if path in routes.handlers:
        return routes.handlers[path]
    return None
