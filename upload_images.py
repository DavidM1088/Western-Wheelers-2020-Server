import cv2
from S3 import S3
from ImageWatermarkRemover import ImageWaterMarkRemover
from os import walk
import os

s3 = S3()

def process(in_file_name):
    image =ImageWaterMarkRemover(in_file_name)
    #cv2.imshow('result', g.img)
    image.remove_watermark()
    image.save()
    #s3.upload_object(image.id + ".png", image.saved_file)


# remove previous output files
#import os, re, os.path
mypath = "./images/output"
for root, dirs, files in os.walk(mypath):
    for file in files:
        fp = os.path.join(root, file)
        #print (fp)
        os.remove(fp)

in_files = []
fs = os.listdir('./images')
count = 0
for fle in fs:
    p = fle.find(".png")
    if p < 0:
        continue
    in_files.append(fle[0: p])
    count += 1
    if count >= 1000:
        break

in_files.sort()

for in_file in in_files:
    print("start process:"+in_file)
    process(in_file)
    #print (id)
    #break


#cv2.waitKey(1000)