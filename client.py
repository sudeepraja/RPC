import client_stub
import sys
import random
K = 100

prev = input()
curr = int(input())

state = random.randint(0,99) 

while True:
	prev_state = client_stub.get_prev(prev)
	print state,prev_state
	if curr == 0:
		if prev_state==state:
			print "Privilege"
			state = (state+1)%K
			print state,prev_state
	else:
		if prev_state!=state:
			print "Privilege"
			state = prev
			print state,prev_state