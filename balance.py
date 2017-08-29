import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2
from time import sleep

import win32api as wapi

train_data = np.load('data/newData.npy')

df = pd.DataFrame(train_data)
print(df.head())
# print(Counter(df[1].apply(str)))

new_data = []
left=[]
right=[]
other=[]

# print(len(train_data))
# shuffle(train_data)

# shuffle(train_data)

# shuffle(train_data)

# shuffle(train_data)
# print(len(train_data))


for data in train_data:
    img = data[0]
    choice = data[1]
    # choice = [ abs(choice[0]), choice[1]]
    # print(img.shape)
    # sleep(0.1)
    # img=img[5:34, 0:80]
    # img=cv2.resize(img, (800,360))
    # cv2.imshow('test',img)
    # sleep(0.1)
    # print(choice)
    # if cv2.waitKey(25) & 0xFF == ord('q') or wapi.GetAsyncKeyState(ord('Q')):
    #   cv2.destroyAllWindows()
    #   break

    # if choice[0]>choice[1]:
    #     left=left+1
    # elif choice[0]<choice[1]: 
    #     right=right+1
    # else:
    #     other=other+1
    # new_data.append([img,choice])


    if choice[0]>choice[1]:
        new_data.append([img, [1.0,0.0]])
    elif choice[0]<choice[1]: 
        new_data.append([img,[0.0,1.0]])
    else:
        new_data.append([img,[0.0,1.0]])
    # new_data.append([img,choice])

# print("left",left)
# print("right", right)
# print("other", other)
# # forwards = forwards[:len(lefts)][:len(rights)]
# print("left ", len(left))
# print("right ", len(right))
# left = left[:len(right)]
# right = right[:len(left)]
# new_data = left + right + other
# print(len(new_data))
# shuffle(new_data)

np.save('data/newDataBinary.npy', new_data)
