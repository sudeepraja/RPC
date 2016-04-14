
import client_stub
import sys
if len(sys.argv) == 2:
	client_stub.name_server = sys.argv[1]

print client_stub.double(10,"127.0.0.1")
print client_stub.abs(10,2,3,"127.0.0.1")
print client_stub.abs(10,2,0,"127.0.0.1")

