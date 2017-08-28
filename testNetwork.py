import numpy as np
import cv2
import time
import os
import win32api as wapi
from time import sleep
from grabScreen import grab_screen, edit_img
from alexnet import alexnet
from vjoy import vj, setJoy

WIDTH = 800
HEIGHT = 360
HEIGHT_OFFSET = 270
WIDTH_SMALL = int(WIDTH/10)
HEIGHT_SMALL = int(HEIGHT/10)
LR = 1e-3
EPOCHS = 8
MODEL_NAME = 'models/track-mania-self-driving-small-net.model'
TURN_TRESHOLD = 0.3
ACCELERATION = -0.6 #its allways negative



def decide_move(moves):
    left=moves[0]
    right=moves[1]
    if abs(left)>TURN_TRESHOLD and abs(left)>right:
        setJoy(left, ACCELERATION, 16000.0)
        print("left")

    elif right>TURN_TRESHOLD:
        setJoy(right, ACCELERATION, 16000.0)
        print("right")
    sleep(0.1)


def test_network():
    last_time = time.time()
    fps=0
    model = alexnet(WIDTH_SMALL, HEIGHT_SMALL, LR)
    for i in list(range(3)):
        print(3-i)
        time.sleep(1)
    paused=False
    print("opening VJ")
    vj.open()

    while(True):
        
        if(not paused):
            
            #get, edit and resize screen image
            screen =  grab_screen(region=(0, HEIGHT_OFFSET, WIDTH, HEIGHT+HEIGHT_OFFSET)) # It is 800x360 window
            screen = edit_img(screen)

            moves=model.predict([screen.reshape(WIDTH_SMALL, HEIGHT_SMALL, 1)])[0]
            
            moves = list(moves)
            print(moves)
            left=moves[0]
            right=moves[1]
            if left>right:
                setJoy(-1.0, ACCELERATION, 16000.0)
                print("left",-left)

            else:
                setJoy(1.0, ACCELERATION, 16000.0)
                print("right")
            sleep(0.2)
            # sleep(0.1)
            fps=fps+1
            # Uncommet for debug mode on run
            # screen=cv2.resize(screen, (WIDTH,HEIGHT))
            # cv2.imshow('window', screen)
            # if ((cv2.waitKey(25) & 0xFF == ord('q')) or wapi.GetAsyncKeyState(ord('Q'))):
            #     print(fps/(time.time()-last_time))
            #     cv2.destroyAllWindows()
            #     break

        if wapi.GetAsyncKeyState(ord('P')):
            paused= not paused
            sleep(0.5)
        if wapi.GetAsyncKeyState(ord('Q')):
            print('Average FPS: ', fps/(time.time()-last_time))
            break
                

if __name__ == "__main__":
    try:
        test_network()
    finally:
        #ALLWAYS CLOSE vJoy!!!
        print("closing VJ")
        vj.close()