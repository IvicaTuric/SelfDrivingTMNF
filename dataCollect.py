import numpy as np
import cv2
import time
import os
import pygame
import win32api as wapi
from time import sleep
from grabScreen import grab_screen, edit_img

WIDTH = 800
HEIGHT = 360
HEIGHT_OFFSET = 270
WIDTH_SMALL = int(WIDTH/10)
HEIGHT_SMALL = int(HEIGHT/10)

# Initialize the joysticks
pygame.init()
pygame.joystick.init()


def seperate_steering(input):
    input_seperated=[0.0,0.0]
    if input<0:
        #left
        input_seperated[0]=input
    else:
        #right
        input_seperated[1]=input
    return input_seperated


def data_collect():
    last_time = time.time()
    fps=0
    for i in list(range(3)):
        print(3-i)
        time.sleep(1)

    traning_file='data/data.npy'

    if os.path.isfile(traning_file):
        print('Resuming old data file ', traning_file)
        training_data = list(np.load(traning_file))
    else:
        print('Starting new data file ', traning_file)
        training_data = []
    last_time = time.time()

    joystick = pygame.joystick.Joystick(1)
    joystick.init()
    print("Recording data from joystick named: ",joystick.get_name())

    while True:
        fps=fps+1

        #get input from joystick
        pygame.event.get()
        steering_input=joystick.get_axis(0)
        input_seperated=seperate_steering(steering_input)

        #get, edit and resize screen image
        screen =  grab_screen(region=(0, HEIGHT_OFFSET, WIDTH, HEIGHT+HEIGHT_OFFSET)) # It is 800x360 window
        screen = edit_img(screen) #Comemnt this out for better FPS

        #Write every 500 frames        
        if len(training_data) % 250==0:
            print('Average FPS: ', fps/(time.time()-last_time))
            print('Traning data size: ',len(training_data))
            np.save(traning_file, training_data)
        training_data.append([screen,input_seperated])
        if wapi.GetAsyncKeyState(ord('Q')):
            print('Average FPS: ', fps/(time.time()-last_time))
            break

        # Uncommet for debug mode on run
        # screen=cv2.resize(screen, (WIDTH,HEIGHT))
        # cv2.imshow('window', screen)
        # if ((cv2.waitKey(25) & 0xFF == ord('q')) or wapi.GetAsyncKeyState(ord('Q'))):
        #     print(fps/(time.time()-last_time))
        #     cv2.destroyAllWindows()
        #     break
        # print("LEFT: ", input_seperated[0], "  RIGHT: ", input_seperated[1]);
        # sleep (0.2)



if __name__ == "__main__":
    data_collect()

