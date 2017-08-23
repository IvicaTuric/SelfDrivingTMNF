import pygame
import win32api as wapi
from time import sleep
pygame.init()
# Initialize the joysticks
pygame.joystick.init()


# -------- Main Program Loop -----------
while True:
    pygame.event.get()        
    joystick = pygame.joystick.Joystick(1)
    joystick.init()
    axes = joystick.get_numaxes()
    steering=joystick.get_axis(0)
    if steering>0:
        print("right")
    else:
        print("left")
    # print(steering)
    sleep(0.1)
    if wapi.GetAsyncKeyState(ord('Q')):
        break
    
pygame.quit ()