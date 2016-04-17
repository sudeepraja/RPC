import client_stub
import sys
if len(sys.argv) == 2:
    client_stub.name_server = sys.argv[1]

print client_stub.f1(10,10,"127.0.0.1")
print client_stub.f2(10,11,12,"127.0.0.1")
print client_stub.f3(30)
print client_stub.f4()

print client_stub.f1(10,0,"127.0.0.1")

