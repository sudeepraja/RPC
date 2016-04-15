
import json
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ForkingMixIn
import server

Function_to_Ip = dict()
IP_to_Function = dict()

class HTTPRequestHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		global Function_to_Ip
		global IP_to_Function

		print "New Conection"
		function = self.headers["Function"]
		data=self.rfile.read(int(self.headers["Content-Length"]))
		print "Data received",data
		x = json.loads(data)

		if function=="register":
			print "Registering", self.client_address[0],x
			IP_to_Function[self.client_address[0]]=set(x)
			for f in x:
				Function_to_Ip[f]=self.client_address[0]
			data="ACK"
			self.send_response(200)
			
		elif function == "deregister":
			print "Deregistering", self.client_address[0],x
			IP_to_Function.pop(self.client_address[0],None)
			for f in x:
				Function_to_Ip.pop(f,None)
			data="ACK"
			self.send_response(200)

		elif function =="get_ip":
			print "Where is",x
			if x in Function_to_Ip:
				data=Function_to_Ip[x]
			else:
				data = "Not Found"
			print x,"is at",data
			self.send_response(404)

		data=json.dumps(data)
		self.send_header('Content-Length',str(len(data)))
		self.end_headers()
		self.wfile.write(data)

TCP_IP = "0.0.0.0"
TCP_PORT = 64321
S = HTTPServer((TCP_IP,TCP_PORT),HTTPRequestHandler)
try:
	S.serve_forever()
except KeyboardInterrupt:
	pass
S.server_close()