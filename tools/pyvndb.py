import json
from socket import socket
import arconfig


class VNDBClient(object):
    addr = "api.vndb.org"
    port = 19534

    def __init__(self, username, passwd):
        self.sock = socket()
        self.sock.connect((self.addr, self.port))
        self.sock.settimeout(1)
        self.login(username, passwd)

    def login(self, username, passwd):
        ans = self.query('login {"protocol":%s,"client":"%s","clientver":%s,'
                         '"username":"%s","password":"%s"}' % (1, "arcueid", 0.1, username, passwd))
        if ans != "ok":
            raise Exception(ans)

    def send(self, string):
        string = bytes("%s\x04" % string, encoding="utf-8")
        self.sock.sendall(string)

    def recv(self):
        ans = b""
        while True:
            s = self.sock.recv(1024)
            ans += s
            if s.endswith(b"\x04"):
                break
        ans = ans.decode("utf-8").rstrip(chr(4))
        return ans.strip()

    def get(self, type, flags, filters):
        ans = self.query("get %s %s (%s)" % (type, flags, filters))

        ans = json.loads(ans.replace("results", "", 1))
        return ans["items"]

    def query(self, string):
        self.send(string)
        recvd = self.recv()
        if recvd.startswith("error"):
            raise Exception(recvd)
        return recvd

    def searchVN(self, name, flags="basic,details,anime,stats"):
        return self.get("vn", flags, 'search~"%s"' % name)


a = VNDBClient("arcueidb", "gnudmsite2")

print(a.searchVN("fate"))
