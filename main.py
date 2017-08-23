import numpy as np
import cv2
from time import sleep
import win32api as wapi
import time
from inputCommands import DecideMove, UP, LEFT, RIGHT, ReleaseKey
from getKeys import key_check
from grabScreen import grab_screen
import os
from alexnet import alexnet

def draw_lines(img,lines):
    if lines!=None:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 5)

def process_img(image):
    original_image = image
    
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # frameResize=np.array([[0,600],[0,230],[800,230],[800,600],[550,600],[470,360],[330,360],[250,600],
    #                      ], np.int32)
    processed_img =  cv2.Canny(processed_img, threshold1 = 200, threshold2=300)
    frameResize=np.array([[250,360],[330,120],[470,120],[550,360]], np.int32)
    # processed_img = roi(processed_img, [frameResize])
    cv2.fillPoly(processed_img, [frameResize], 0)
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
    lines = cv2.HoughLinesP(processed_img, 0.9, np.pi/180, 80, 20, 10)
    # print(len(lines))
    # sleep(0.5)
    draw_lines(processed_img,lines)
    return processed_img

def main():
    last_time = time.time()
    fps=0
    # for i in list(range(3)):
    #     print(3-i)
    #     time.sleep(1)

    # traning_file='shit.npy'

    # if os.path.isfile(traning_file):
    #     print('File exists, loading previous data!')
    #     training_data = list(np.load(traning_file))
    # else:
    #     print('File does not exist, starting fresh!')
    #     training_data = []
    last_time = time.time()

    while True:
        fps=fps+1
        screen =  grab_screen(region=(0,270,800,630))
        screen = process_img(screen)
        # screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen=cv2.resize(screen, (80,36))
        screen=cv2.resize(screen, (800,360))
        cv2.imshow('window', screen)
        # screen=screen[5:34, 0:80]
        #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if ((cv2.waitKey(25) & 0xFF == ord('q')) or wapi.GetAsyncKeyState(ord('Q'))):
            print(fps/(time.time()-last_time))
            cv2.destroyAllWindows()
            break
        # if len(training_data) % 250==0:
        #     print('Average FPS: ', fps/(time.time()-last_time))
        #     print('Traning data size: ',len(training_data))
        #     np.save(traning_file, training_data)
        # training_data.append([screen,key_check()])

WIDTH = 80
HEIGHT = 29
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
    main()

# if __name__ == '__main__':
#     time.sleep(2)
#     PressKey(UP)
#     time.sleep(1)
#     ReleaseKey(UP)
#     time.sleep(1)
