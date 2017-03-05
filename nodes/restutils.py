import httplib
import json
import requests


class EAGERRest(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def setRandomizeTo(self, randomize):
        data = {
            "randomize": str(randomize)
        }
        ret = self.rest_call('/wm/randomizer/config/json', data, 'POST')
        return ret[0] == 200

    def enableRandomizer(self):
        data = {}
        ret = self.rest_call('/wm/randomizer/module/enable/json', data, 'POST')
        return ret[0] == 200

    def disableRandomizer(self):
        data = {}
        ret = self.rest_call('/wm/randomizer/module/disable/json', data, 'POST')
        return ret[0] == 200

    def addServer(self, server):
        data = {
            "server": server
        }
        ret = self.rest_call('/wm/randomizer/server/add/json', data, 'POST')
        return ret[0] == 200

    def removeServer(self, server):
        data = {
            "server": server
        }
        ret = self.rest_call('/wm/randomizer/server/remove/json', data, 'POST')
        return ret[0] == 200

    def addPrefix(self, ip, mask, server):
        data = {
            "ip-address": ip,
            "mask": mask,
            "server": server
        }
        ret = self.rest_call('/wm/randomizer/prefix/add/json', data, 'POST')
        return ret[0] == 200

    def removePrefix(self, ip, mask, server):
        data = {
            "ip-address": ip,
            "mask": mask,
            "server": server
        }
        ret = self.rest_call('/wm/randomizer/prefix/remove/json', data, 'POST')
        return ret[0] == 200

    def setLanPort(self, port):
        data = {
            "localport": str(port)
        }
        ret = self.rest_call('/wm/randomizer/config/json', data, 'POST')
        return ret[0] == 200

    def setWanPort(self, port):
        data = {
            "wanport": str(port)
        }
        ret = self.rest_call('/wm/randomizer/config/json', data, 'POST')
        return ret[0] == 200

    def rest_call(self, path, data, action):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        body = json.dumps(data)
        url = 'http://' + str(self.ip) + ':' + str(self.port) + path
        ret = requests.post(url, headers=headers, data=body)
        print ret
        return ret
        # conn = httplib.HTTPConnection(self.ip, self.port)
        # print 'host: ' + str(conn.host)
        # print 'port: ' + str(conn.port)
        # print 'timeout: ' + str(conn.timeout)
        # print 'source_address: ' + str(conn.source_address)
        # print 'socket: ' + str(conn.sock)
        # conn.request(action, path, body, headers)
        # response = conn.getresponse()
        # ret = (response.status, response.reason, response.read())
        # print ret
        # conn.close()
        # return ret
