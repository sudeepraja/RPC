
import client_stub
import sys
import fcntl
import random
prev_ip = sys.argv[1]
system_number = sys.argv[2]

K=100
state = random.randint(0,100)%K

def obtain_lock():
	x = open('state', 'r+')
	fcntl.flock(x, fcntl.LOCK_EX)
	return x

def release_lock(x):
	fcntl.flock(x,fcntl.LOCK_U)
	x.close()


x=obtain_lock()
x.write(str(state))
release_lock(x)

while True:
	predessor_state = client_stub.get_value()
	x=obtain_lock()
	state = int(x.read().strip())
	if system_number == 0:
		if state == predessor_state:
			state = (state +1)%K
	else:
		if state != predessor_state:
			state = predessor_state
	x.seek(0)
	x.write(str(state))
	x.truncate()
	release_lock(x)






