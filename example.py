from vjoy import vj, setJoy
import numpy as np
import time

import win32api as wapi

print("vj opening", flush=True)
vj.open()

time.sleep(1)


print("sending axes", flush=True)

# valueX, valueY between -1.0 and 1.0q
# scale between 0 and 16000
scale = 16000.0
while True:
	print("LEFT")
	for i in range(0,20,1):
	    setJoy(-1.0, -0.5, scale)
	    time.sleep(0.05)
	print("RIGHT")
	if wapi.GetAsyncKeyState(ord('Q')):
		break
	for i in range(0,20,1):
	    setJoy(1.0, -0.5, scale)
	    time.sleep(0.05)
	if wapi.GetAsyncKeyState(ord('Q')):
		break

print("vj closing", flush=True)
vj.close()