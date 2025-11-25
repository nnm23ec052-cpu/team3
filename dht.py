import usocket
import ussl

def request(method, url, data=None, json=None, headers={}):
    proto, dummy, host, path = url.split("/", 3)
    if proto == "http:":
        port = 80
        ssl = False
    elif proto == "https:":
        port = 443
        ssl = True
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    addr = usocket.getaddrinfo(host, port)[0][-1]
    s = usocket.socket()
    s.connect(addr)

    if ssl:
        s = ussl.wrap_socket(s)

    s.write("{} /{} HTTP/1.0\r\n".format(method, path))
    s.write("Host: {}\r\n".format(host))

    if json is not None:
        import ujson
        data = ujson.dumps(json)
        headers["Content-Type"] = "application/json"

    if data:
        headers["Content-Length"] = str(len(data))

    for k in headers:
        s.write("{}: {}\r\n".format(k, headers[k]))

    s.write("\r\n")

    if data:
        s.write(data)

    line = s.readline()
    protover, status, msg = line.split(None, 2)
    status = int(status)

    while True:
        line = s.readline()
        if line == b"\r\n" or line == b"":
            break

    return Response(s, status)


def get(url, **kw):
    return request("GET", url, **kw)


def post(url, **kw):
    return request("POST", url, **kw)


class Response:

    def init(self, sock, status):
        self.raw = sock
        self.status_code = status

    def close(self):
        if self.raw:
            self.raw.close()
            self.raw = None

    @property
    def text(self):
        return str(self.raw.read(), "utf-8")

    def json(self):
        import ujson
        return ujson.loads(self.raw.read())
