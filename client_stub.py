import httplib
import json
import sys
name_server = None




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

def double( p1,ip=None ):
	if ip==None:
		ip=ask_name_server("double")
	data=json.dumps({'p1':p1})
	return make_rpc_call(data,ip,"double")



def abs( p1, p2, p3,ip):
	data=json.dumps({'p1':p1, 'p2':p2, 'p3':p3})
	return make_rpc_call(data,ip,"abs")



