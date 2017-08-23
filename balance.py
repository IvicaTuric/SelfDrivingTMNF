import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2
from time import sleep

train_data = np.load('training_data_v3.npy')

df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[1].apply(str)))

lefts = []
rights = []
forwards = []

# shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]
    
    print(img.shape)
    sleep(10)

    # img=img[5:34, 0:80]
    # img=cv2.resize(img, (800,290))
    cv2.imshow('test',img)
    # sleep(0.1)
    print(choice)
    # if cv2.waitKey(25) & 0xFF == ord('q'):
    # 	cv2.destroyAllWindows()
    # 	break
#     if choice == [1,0,0]:
#         lefts.append([img,[1,0,0]])
#     elif choice == [0,1,0]:
#         forwards.append([img,[0,1,0]])
#     elif choice == [0,0,1]:
#         rights.append([img,[0,0,1]])
#     else:
#         print('no matches')


# forwards = forwards[:len(lefts)][:len(rights)]
# lefts = lefts[:len(forwards)]
# rights = rights[:len(forwards)]

# final_data = forwards + lefts + rights
# shuffle(final_data)

# np.save('training_data_v3.npy', final_data)