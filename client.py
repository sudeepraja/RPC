
import client_stub
import sys
client_stub.name_server = sys.argv[1]

print client_stub.abs(3,4,5,"127.0.0.1")

print client_stub.double(3,"127.0.0.1")
print client_stub.double(4)