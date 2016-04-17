
import client_stub
import sys
if len(sys.argv) == 2:
    client_stub.name_server = sys.argv[1]

print client_stub.f1(10,10,"127.0.0.1")

