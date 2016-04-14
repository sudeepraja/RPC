
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
	response = conn.getresponse().read()
	ip = json.loads(response)
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

def double( p1,ip=None ):
	if ip==None:
		ip=ask_name_server("double")
	data=json.dumps({'p1':p1})
	return make_rpc_call(data,ip,"double")



def abs( p1, p2, p3,ip):
	data=json.dumps({'p1':p1, 'p2':p2, 'p3':p3})
	return make_rpc_call(data,ip,"abs")



