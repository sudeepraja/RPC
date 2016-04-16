
import client_stub
import sys
if len(sys.argv) == 2:
	client_stub.name_server = sys.argv[1]

print client_stub.f1(3,4)
print client_stub.f2(3,4)
print client_stub.f3(3,4)
print client_stub.g1(3,4,5)
print client_stub.g2(3,4,5)
print client_stub.g3(3,4,5)
print client_stub.h1()
print client_stub.h2()
print client_stub.h3()

