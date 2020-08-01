import cv2
import numpy as np
import copy
import random
import os
import time

def get_brightness_score(pix):
    white = 0
    for i in range(3):
        white += pix[i]
    return white

def get_diff(p1, p2):
    diff = 0
    for i in range(3):
        diff = abs(p2[i] - p1[i])
    return diff

def is_same(p1, p2):
    for i in range(3):
        if p1[i] != p2[i]:
            return False
    return True

row_avg = []

def monochrome_score(pix):
    score = np.std(pix)
    # score = abs(pix[1] - pix[0])
    # #print(p[0], p[1], p[2])
    # x = pix[2]
    # y = pix[1]
    # x = x - pix[1]
    # score += x
    # score += abs(p[2] - p[0])
    return score

def is_title(img, r, c):
    if get_brightness_score(img[r, c]) < 400:
        return False
    ms = monochrome_score(img[r, c])
    if ms >2.0:
        return False
    return True

def test(img, row_start, row_end, col_start, col_end):
    result = copy.deepcopy(img)
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            if is_title(img, r, c):
                result[r, c] = (0, 200, 0)
                avg = [0,0,0]
                cnt = 0
                span = 20
                for d in range(0, span):
                    if not is_title(img, r-d, c):
                        ni = img[r-d, c]
                        avg += ni
                        cnt += 1
                        #break
                if cnt > 0:
                    avg = avg // cnt
                max = 6
                r1 = random.randint(-max, max)
                #r2 = random.randint(-max, max)
                #r3 = random.randint(-max, max)
                avg[0] += r1
                avg[1] += r1
                avg[2] += r1

                span = 3
                span += random.randint(0, 2)
                for rn in range(-span, span):
                    for cn in range(-span, span):
                        result[r+rn, c+cn] = avg

    return result

def process(img):
    for r in range(row_start, row_end, col_start, col_end):
        darks = []
        same_cnt = 0
        same_start = None
        in_let = False
        last = None
        if (r % 100 == 0):
            print("row:" + str(r))

        c = col_start
        for r in range(row_start, row_end, col_start, col_end):
            if not last is None:
                s1 = get_score(img[r, c])
                s2 = get_score(last)
                if abs(s1 - s2) < 19 and monochrome_score(img[r, c]) < 3:
                    # if str(img[r, c]) == str(last):
                    same_cnt += 1
                else:
                    same_start = c
                    same_cnt = 0
            last = img[r, c]

            dark = 0

            if same_cnt > 4:
                # print ("found run")
                val = img[r, c - same_cnt - 38]
                right = 10;
                left = 10;
                if same_start is not None:
                    for cx in range(same_start - left, c + right):
                        if cx < cols:
                            img[r, cx] = val  # (0,127,0) #val
                            # pass
                c += right + 1
                same_cnt = 0
                same_start = 0
                same_start = None

            else:
                c += 1

            # if c==col_start+1 or c==col_end-1:
            #     img[r, c] = (0,0,0)

        # if (r == row_start or r == row_end-1):
        #     for rx in range(2):
        #         for c in range(cols):
        #             img[r+rx, c] = (0,0,0)

def process_file(fle):
    ##img = cv2.imread('images/pm10.png')
    img = cv2.imread(fle)
    rows, cols, colors = img.shape
    print ("rows ", rows, cols)
    row_edge = rows // 5
    row_start = row_edge
    row_end = rows - row_edge
    col_start = cols // 3
    col_end = 2 * col_start
    light_threshold = 3 * 230
    dark_threshold = 3 * 180

    #process(img)
    row_start = int(rows * 0.4)
    row_end = int(rows * 0.7)
    col_start = int(rows * 0.4)
    col_end = int(rows * 0.6)

    result = test(img, row_start, row_end, col_start, col_end)

    d1 = {}
    d2 = {}
    #cv2.imshow('im1', img)
    cv2.imshow('im2', result)
    #cv2.imwrite('result.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

dir = '../../Desktop'
done = os.listdir(dir)
for i in range(4000000):
    entries = os.listdir('../../Desktop')
    for e in entries:
        #print (e)
        nm = dir +'/'+e
        if e in done:
            time.sleep(0.1)
            print ('...', i)
            continue

        process_file(nm)
        print("DONE:" + e)
        done.append(e)
        continue
