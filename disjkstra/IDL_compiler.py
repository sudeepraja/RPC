import sys
import re

def generate_client_stub(client_stub_file,f):
    pub = f[0]
    function_name = f[1]
    arguments = f[2:]
    if len(arguments) != len(set(arguments)):
        print "In",function_name,"arguments must be unique"
        sys.exit(0)

    comma = ", "
    if len(arguments)==0:
        comma=" "
    if pub == "publish":
        print >>client_stub_file, "def "+function_name+"( "+", ".join(arguments)+comma+"ip=None ):"
        print >>client_stub_file, "\t"+'if ip==None:'
        print >>client_stub_file, "\t\t"+'ip=ask_name_server("'+function_name+'")'

    elif pub == "nopublish":
        print >>client_stub_file, "def "+function_name+"( "+", ".join(arguments)+comma+"ip):"

    else:
        print "Error, need to specify publish or nopublih"
        exit(0)

    dictionary_string = ["'"+f+"':"+f for f in arguments]
    if len(arguments)!=0:
        print >>client_stub_file, "\t"+"data=json.dumps({"+", ".join(dictionary_string)+"})"
    else:
        print >>client_stub_file, "\t"+"data=json.dumps('')"
    print >>client_stub_file, "\t"+'return make_rpc_call(data,ip,"'+function_name+'")'
    print >>client_stub_file, "\n\n"


input_file = file(sys.argv[1])
functions = [line.strip() for line in input_file.readlines()]

client_stub_file = open("client_stub.py","w")

print >>client_stub_file, """
import httplib
import json
import sys
import traceback
name_server = None

def ask_name_server(x):
    if name_server == None:
        print "Name server not specified"
        sys.exit(0)
    print "Asking Name Server for",x
    conn = httplib.HTTPConnection(name_server,64321)
    data=json.dumps(x)
    conn.request("POST", "",data,{"Content-Length": str(len(data)),"Content-type":"application/json","Function":"get_ip"})
    response = conn.getresponse()
    status = response.status
    if status == 200:
        ip = json.loads(response.read())
    elif status == 404:
        print "Function",x,"not found at "
        conn.close()
        sys.exit(0)
    conn.close()
    print "Function is at",ip
    return ip

def make_rpc_call(data,ip,func_name):
    conn = httplib.HTTPConnection(ip,12346)
    conn.request("POST", "",data,{"Content-Length": str(len(data)),"Content-type":"application/json","Function":func_name})
    response = conn.getresponse()
    status = response.status
    if status == 200:
        answer = json.loads(response.read())
    elif status == 404:
        print "Function",func_name,"not found at ",ip
        conn.close()
        sys.exit(0)
    elif status == 400:
        traceback.print_stack()
        print json.loads(response.read())
        conn.close()
        sys.exit(0)
    conn.close()
    return answer
"""
publish_function_names=[]
all_function_names=set()
for func in functions:
    pattern = re.compile("(\w+)\s+(\w+)\((\s*\w+\s*,)*(\s*\w+\s*)\)|(\w+)\s+(\w+)(\(\s*\))")
    if func.strip()=="":
        pass
    elif pattern.match(func):
        f=re.compile("[ ,()]").split(func)
        f=[x for x in f if x!=""]
        generate_client_stub(client_stub_file,f)
        if f[0]=="publish":
            publish_function_names.append("'"+f[1]+"'")
        if "'"+f[1]+"'" not in all_function_names:
            all_function_names.add("'"+f[1]+"'")
        else:
            print f[1] ,"already defined"
            sys.exit(0)
    else:
        print "Syntax Error"
        sys.exit(0)
    

client_stub_file.close()


server_stub_file = open("server_stub.py","w")
print >>server_stub_file,"""
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

"""

print >>server_stub_file,"publish_function_list=["+", ".join(publish_function_names)+"]"
print >>server_stub_file,"all_function_list=["+", ".join(all_function_names)+"]"

print >>server_stub_file,"""
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
"""
server_stub_file.close()


server_file = open("server.py","w")
for func in functions:
    if func.strip()!="":
        f=re.compile("[ ,()]").split(func)
        f=[x for x in f if x!=""]
        function_name = f[1]
        arguments = f[2:]
        print >>server_file, "def "+function_name+"( "+", ".join(arguments)+" ):"
        print >>server_file, "\tpass\n\n"
    else:
        pass
server_file.close()

client_file = open("client.py","w")
print >>client_file,"""
import client_stub
import sys
if len(sys.argv) == 2:
    client_stub.name_server = sys.argv[1]
"""

client_file.close()