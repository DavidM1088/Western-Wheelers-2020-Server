import cv2
from S3 import S3
from Image_G import Image_G
from os import walk
import os

def process(id):
    g = Image_G(id)
    #cv2.imshow('result', g.img)
    g.process()
    g.save()
    s3 = S3()
    #s3.upload_file(g.id, g.saved_file)

ids = []
fs = os.listdir('./images')
for fle in fs:
    p = fle.find(".png")
    if p < 0:
        continue
    id = fle[0: p]
    ids.append(id)

ids.sort()

for id in ids:
    print("process:"+id)
    process(id)
    print (id)
    break


#cv2.waitKey(1000)