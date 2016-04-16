
import json
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ForkingMixIn
import server
import sys
import httplib
import traceback

class ThreadedHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print "New Conection"
        data=self.rfile.read(int(self.headers["Content-Length"]))
        print "Data received",data
        x = json.loads(data)
        if self.headers["Function"] in dir(server):
            try:
                if len(x)!=0:
                    res = getattr(server, self.headers["Function"])(**x)
                else:
                    res = getattr(server, self.headers["Function"])()               
                self.send_response(200)
            except Exception as e:
                res = traceback.format_exc().splitlines()[-1]
                self.send_response(400)
        else:
            res = "Function not available"
            self.send_response(404)
        data = json.dumps(res)
        self.send_header('Content-Length',str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        print "Data sent: ",data
        return
        
class ThreadedHTTPServer(ForkingMixIn, HTTPServer):
    pass

TCP_IP = "0.0.0.0"
TCP_PORT = 12346


publish_function_list=['f1', 'f2', 'f3', 'g1', 'g2', 'g3', 'h1', 'h2', 'h3']
all_function_list=['f2', 'h3', 'h2', 'g3', 'g2', 'h1', 'g1', 'f1', 'f3']

if len(sys.argv) == 2:
    Name_server_ip = sys.argv[1]
    Name_server_port = 64321
    conn = httplib.HTTPConnection(Name_server_ip,Name_server_port)

    data=json.dumps(publish_function_list)
    conn.request("POST", "",data,{"Content-Length": str(len(data)),"Content-type":"application/json","Function":"register"})
    response = json.loads(conn.getresponse().read())
    if response=="ACK":
        print "Functions Registered and Server Starting"
    conn.close()
else:
    print "Starting without name server"

S = ThreadedHTTPServer((TCP_IP,TCP_PORT),ThreadedHTTPRequestHandler)
try:
    S.serve_forever()
except KeyboardInterrupt:
    pass

if len(sys.argv) == 2:
    conn.request("POST", "",data,{"Content-Length": str(len(data)),"Content-type":"application/json","Function":"deregister"})
    response = json.loads(conn.getresponse().read())
    if response=="ACK":
        print "Functions Deregistered and Server Closing"
    conn.close()
S.server_close()

