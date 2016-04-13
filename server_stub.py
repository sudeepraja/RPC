
import json
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ForkingMixIn
import server
import sys
import httplib

class ThreadedHTTPRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print "New Conection"
		data=self.rfile.read(int(self.headers["Content-Length"]))
		print "Data received",data
		x = json.loads(data)
		if self.headers["Function"] in dir(server):
			res = getattr(server, self.headers["Function"])(**x)
			self.send_response(200)
		else:
			res = "Function not available"
			self.send_response(404)
		data = json.dumps(res)
		self.send_header('Content-Length',str(len(data)))
		self.end_headers()
		self.wfile.write(data)
		print "Data sent: ",data
		
class ThreadedHTTPServer(ForkingMixIn, HTTPServer):
	pass

TCP_IP = "0.0.0.0"
TCP_PORT = 12346


Name_server_ip = sys.argv[1]
Name_server_port = 64321
conn = httplib.HTTPConnection(Name_server_ip,Name_server_port)

publish_function_list=['double']
all_function_list=['double', 'abs']

data=json.dumps(publish_function_list)
conn.request("GET", "",data,{"Content-Length": str(len(data)),"Content-type":"application/json","Function":"register"})
response = json.loads(conn.getresponse().read())
if response=="ACK":
	print "Functions Registered and Server Starting"
conn.close()

S = ThreadedHTTPServer((TCP_IP,TCP_PORT),ThreadedHTTPRequestHandler)
try:
	S.serve_forever()
except KeyboardInterrupt:
	pass

conn.request("GET", "",data,{"Content-Length": str(len(data)),"Content-type":"application/json","Function":"deregister"})
response = json.loads(conn.getresponse().read())
if response=="ACK":
	print "Functions Deregistered and Server Closing"
conn.close()
S.server_close()

