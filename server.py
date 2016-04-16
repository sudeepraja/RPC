import fcntl
def obtain_lock():
	x = open('state', 'r+')
	fcntl.flock(x, fcntl.LOCK_EX)
	return x

def release_lock(x):
	fcntl.flock(x,fcntl.LOCK_U)
	x.close()

def get_value():
	x=obtain_lock()
	state = int(x.read().strip()
	release_lock(x)
	return state
