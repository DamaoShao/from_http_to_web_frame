import socket
import urllib.parse

from routes import route_static, route_dict


class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def add_cookies(self):
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        self.headers = {}
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        self.cookies = {}
        self.add_cookies()

    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f


request = Request()


ERROR = {
    '404': b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'
}


def parsed_path(path):
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    r = {
        '/static': route_static,
    }
    r.update(route_dict)
    response = r.get(path)
    if response:
        return response(request)
    else:
        return ERROR['404']


def run(host='', port=2000):
    print("http://{}:{}".format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            print("*"*50)
            s.listen(3)
            connection, address = s.accept()
            r = connection.recv(1000)
            r = r.decode('utf-8')
            # filter empty
            if len(r.split()) < 2:
                continue
            else:
                print("***Request:\n{0}\n***".format(r))
            path = r.split()[1]
            request.method = r.split()[0]
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
            request.body = r.split('\r\n\r\n', 1)[1]
            response = response_for_path(path)
            connection.sendall(response)
            try:
                print("***Response:\n{0}***".format(bytes.decode(response)))
            except Exception:
                pass
            connection.close()


if __name__ == '__main__':
    run(host='127.0.0.1', port=8080)
