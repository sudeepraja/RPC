
import client_stub
import sys
import fcntl
import random
import time
prev_ip = sys.argv[1]
system_number = int(sys.argv[2])

K=100
state = random.randint(0,100)%K

def obtain_lock():
	x = open('state', 'r+')
	fcntl.flock(x, fcntl.LOCK_EX)
	return x

def release_lock(x):
	fcntl.flock(x,fcntl.LOCK_UN)
	x.close()


x = open('state', 'w')
x.write(str(state))
x.close()

while True:
	time.sleep(5)
	predessor_state = client_stub.get_value(prev_ip)
	x=obtain_lock()
	state = int(x.read().strip())
	print state, predessor_state
	if system_number == 0:
		if state == predessor_state:
			print "Privilege"
			state = (state +1)%K
	else:
		if state != predessor_state:
			print "Privilege"
			state = predessor_state
	x.seek(0)
	x.write(str(state))
	x.truncate()
	release_lock(x)






