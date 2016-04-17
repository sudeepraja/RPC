
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

def get_value(  ip):
	data=json.dumps('')
	return make_rpc_call(data,ip,"get_value")



