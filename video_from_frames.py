#importing the necessary libraries
import cv2
import os

#creating a list of images
image_list = []

#looping through the images in the directory
# for image in os.listdir('video'):
#     print(image)
#     image_list.append(cv2.imread('video/' + image))
for i in range(500):
    print(i)
    image_list.append(cv2.imread(f'video/{i}.jpeg'))
for i in range(500):
    print(i)
    image_list.append(cv2.imread(f'video/{499-i}.jpeg'))
#setting the frame rate
frame_rate = 25
#defining the output video
out = cv2.VideoWriter('fractal zoom 4-23 -23.mp4',cv2.VideoWriter_fourcc(*'DIVX'), frame_rate, (image_list[0].shape[1], image_list[0].shape[0]))
#looping through the images in the list
for image in image_list:
    out.write(image)
#releasing the output
out.release()