# encoding: utf-8

import socket


class HttpRequest(object):
    @staticmethod
    def parse_url(url):
        """
        :param url: http://www.example.com/example
        :return: (host, port, path) -> ("www.example.com", "80", "/example")
        """
        urls = url.split("://")[1].split("/", 1)
        if len(urls) == 1:
            return urls[0], 80, "/"
        if ":" in urls[0]:
            host, port = urls[0].split(":")
            return host, int(port), "/" + urls[1]
        return urls[0], 80, "/" + urls[1]

    @staticmethod
    def get_resp(s):
        resp = b''
        buffer_size = 1024
        while True:
            r = s.recv(buffer_size)
            if len(r) == 0:
                break
            resp += r
        return resp

    @staticmethod
    def parse_resp(resp):
        """
        :param resp:
        :return: http_status_code -> int, headers -> dict, body -> str
        """
        header, body = resp.split(b'\r\n\r\n', 1)
        _headers = header.split(b'\r\n')
        http_status_code = int(_headers[0].split()[1])
        headers = dict(line.split(b': ') for line in _headers[1:])
        return http_status_code, headers, body

    def requests(self, method, url):
        host, port, path = self.parse_url(url)
        print(host, port, path)
        s = socket.socket()
        s.connect((host, port))
        request_data = '{method} {path} HTTP/1.1\r\nhost: {host}\r\nConnection: close\r\n\r\n'.format(
            method=method.upper(), path=path, host=host)
        print("***Requests:\n{}\n***".format(request_data))
        s.send(request_data.encode('utf-8'))
        resp = self.get_resp(s)
        http_status_code, headers, body = self.parse_resp(resp)
        print("***Response code:\n{}\n***".format(http_status_code))
        print("***Response headers:\n{}\n***".format(headers))
        print("***Response body:\n{}\n***".format(body))
        if 300 <= http_status_code < 400:
            return self.requests(method, headers["Location"])
        return http_status_code, headers, body

    def get(self, url):
        return self.requests('get', url)

    def post(self, url):
        return self.requests('post', url)


if __name__ == '__main__':
    requests = HttpRequest()
    requests.get('http://www.example.com')
    # demo_requests.get('http://127.0.0.1:8080/login')
