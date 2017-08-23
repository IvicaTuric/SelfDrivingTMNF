import numpy as np
import cv2
import time
import os
import pygame
import win32api as wapi
from time import sleep
from grabScreen import grab_screen
from alexnet import alexnet

WIDTH = 800
HEIGHT = 360
HEIGHT_OFFSET = 270

# Initialize the joysticks
pygame.init()
pygame.joystick.init()


def edit_img(image):    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image =  cv2.Canny(image, threshold1 = 200, threshold2=300)
    frameResize=np.array([[250,360],[330,120],[470,120],[550,360]], np.int32)
    cv2.fillPoly(image, [frameResize], 0)
    image = cv2.GaussianBlur(image,(5,5),0)
    lines = cv2.HoughLinesP(image, 0.9, np.pi/180, 80, 20, 10)
    if lines!=None:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 5)
    return image


def seperate_steering(input):
    input_seperated=[0.0,0.0]
    if input<0:
        #left
        input_seperated[0]=abs(input)
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

    traning_file='data/shit.npy'

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
        sleep(0.2)

        #get input from joystick
        pygame.event.get()
        steering_input=joystick.get_axis(0)
        input_seperated=seperate_steering(steering_input)
        print("LEFT: ", input_seperated[0], "  RIGHT: ", input_seperated[1]);

        #get and edit screen image
        screen =  grab_screen(region=(0,HEIGHT_OFFSET,WIDTH,HEIGHT+HEIGHT_OFFSET)) # It is 800x360 window
        screen = edit_img(screen) #Comemnt this out for better FPS
        screen=cv2.resize(screen, (WIDTH/10,HEIGHT/10))
        cv2.imshow('window', screen)
        
        if ((cv2.waitKey(25) & 0xFF == ord('q')) or wapi.GetAsyncKeyState(ord('Q'))):
            print(fps/(time.time()-last_time))
            cv2.destroyAllWindows()
            break

        # if wapi.GetAsyncKeyState(ord('Q'))):
        #     print(fps/(time.time()-last_time))
        #     break

        # if len(training_data) % 250==0:
        #     print('Average FPS: ', fps/(time.time()-last_time))
        #     print('Traning data size: ',len(training_data))
        #     np.save(traning_file, training_data)
        # training_data.append([screen,])


LR = 1e-3
EPOCHS = 8
MODEL_NAME = 'track-mania-self-driving-big.model'

def maintest():
    last_time = time.time()
    fps=0
    model = alexnet(WIDTH, HEIGHT, LR)
    # for i in list(range(3)):
    #     print(3-i)
    #     time.sleep(1)
    paused=False
    while(True):
        if(not paused):
            # 800x600 windowed mode
            screen =  grab_screen(region=(0,300,800,640))
            # print('loop took {} seconds'.format(time.time()-last_time))
            # last_time = time.time()
            # new_screen = process_img(screen)
            screen=cv2.resize(screen, (WIDTH,HEIGHT))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            cv2.imshow('window', screen)
            # screen = cv2.resize(screen, (80,60))
            # cv2.imshow('',screen)
            predi=model.predict([screen.reshape(WIDTH,HEIGHT,1)])[0]
            print(predi)
            moves = list(predi)
            print(moves)
            # sleep(0.1)
            DecideMove(moves)
            if ((cv2.waitKey(25) & 0xFF == ord('q')) or wapi.GetAsyncKeyState(ord('Q'))):
                print(fps/(time.time()-last_time))
                cv2.destroyAllWindows()
                break
        if wapi.GetAsyncKeyState(ord('P')):
            paused= not paused
            ReleaseKey(UP)
            ReleaseKey(LEFT)
            ReleaseKey(RIGHT)
            sleep(0.5)


if __name__ == "__main__":
    data_collect()

# if __name__ == '__main__':
#     time.sleep(2)
#     PressKey(UP)
#     time.sleep(1)
#     ReleaseKey(UP)
#     time.sleep(1)
