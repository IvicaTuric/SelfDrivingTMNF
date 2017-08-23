import win32api as wapi
from win32con import VK_UP, VK_LEFT, VK_RIGHT
import time
from msvcrt import getch

keyList = [VK_UP, VK_LEFT, VK_RIGHT]

def key_check():
	keysPressed=[]
	out=[0,0,0]
	for key in keyList:
		if wapi.GetAsyncKeyState(key):
			keysPressed.append(key)
	
	if VK_LEFT in keysPressed:
		out[0]=1
	elif VK_RIGHT in keysPressed:
		out[2]=1
	else:
		out[1]=1
	return out