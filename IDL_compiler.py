import sys
import re


def generate_client_stub(client_stub_file,f):
	pub = f[0]
	function_name = f[1]
	arguments = f[2:]

	if pub == "publish":
		print >>client_stub_file, "def "+function_name+"( "+", ".join(arguments)+",ip=None ):"
		print >>client_stub_file, "\t"+'if ip==None:'
		print >>client_stub_file, "\t\t"+'ip=ask_name_server("'+function_name+'")'

	elif pub == "nopublish":
		print >>client_stub_file, "def "+function_name+"( "+", ".join(arguments)+",ip):"

	else:
		print "Error, need to specify publish or unpublih"
		exit(0)

	dictionary_string = ["'"+f+"':"+f for f in arguments]
	print >>client_stub_file, "\t"+"data=json.dumps({"+", ".join(dictionary_string)+"})"
	print >>client_stub_file, "\t"+'return make_rpc_call(data,ip,"'+function_name+'")'
	print >>client_stub_file, "\n\n"


input_file = file(sys.argv[1])
functions = [line.strip() for line in input_file.readlines()]

client_stub_file = open("client_stub.py","w")
print >>client_stub_file, "import httplib"
print >>client_stub_file, "import json"
print >>client_stub_file, "import sys"
print >>client_stub_file, "name_server = None"
print >>client_stub_file, "\n\n"

print >>client_stub_file, """
def ask_name_server(x):
	print "Asking Name Server for",x
	conn = httplib.HTTPConnection(name_server,64321)
	data=json.dumps(x)
	conn.request("GET", "",data,{"Content-Length": str(len(data)),"Content-type":"application/json","Function":"get_ip"})
	response = conn.getresponse().read()
	ip = json.loads(response)
	conn.close()
	print "Function is at",ip
	return ip

def make_rpc_call(data,ip,func_name):
	conn = httplib.HTTPConnection(ip,12346)
	conn.request("GET", "",data,{"Content-Length": str(len(data)),"Content-type":"application/json","Function":func_name})
	response = conn.getresponse().read()
	answer = json.loads(response)
	conn.close()
	return answer
"""
publish_function_names=[]
all_function_names=[]
for func in functions:
	f=re.compile("[ ,()]").split(func)
	f=[x for x in f if x!=""]
	generate_client_stub(client_stub_file,f)
	if f[0]=="publish":
		publish_function_names.append("'"+f[1]+"'")
	all_function_names.append("'"+f[1]+"'")
	

client_stub_file.close()


server_stub_file = open("server_stub.py","w")
print >>server_stub_file,"""
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
"""

print >>server_stub_file,"publish_function_list=["+", ".join(publish_function_names)+"]"
print >>server_stub_file,"all_function_list=["+", ".join(all_function_names)+"]"

print >>server_stub_file,"""
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
"""
server_stub_file.close()


server_file = open("server.py","w")
for func in functions:
	f=re.compile("[ ,()]").split(func)
	f=[x for x in f if x!=""]
	function_name = f[1]
	arguments = f[2:]
	print >>server_file, "def "+function_name+"( "+", ".join(arguments)+" ):"
	print >>server_file, "\tpass\n\n"
server_file.close()

client_file = open("client.py","w")
print >>client_file,"""
import client_stub
import sys
client_stub.name_server = sys.argv[1]
"""

client_file.close()