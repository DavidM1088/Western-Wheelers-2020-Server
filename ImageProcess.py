import cv2
import numpy as np
import math




def get_score(pix):
    white = 0
    for i in range(3):
        white += pix[i]
    return white


def get_diff(p1, p2):
    diff = 0
    for i in range(3):
        diff = abs(p2[i] - p1[i])
    return diff


light_threshold = 3 * 230
dark_threshold = 3 * 180


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

def process():
    for r in range(row_start, row_end):
        darks = []
        same_cnt = 0
        same_start = None
        in_let = False
        last = None
        if (r % 100 == 0):
            print("row:" + str(r))

        c = col_start
        while c < col_end:
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

img = cv2.imread('images/pm5.png')
rows, cols, colors = img.shape
cv2.imshow('result', img)
cv2.waitKey(180000)
row_edge = rows // 5
row_start = row_edge
row_end = rows - row_edge
col_start = cols // 3
col_end = 2 * col_start
# row_start = 0
# row_end = rows
# col_start = 0
# col_end = cols

print(rows, cols)
# img[0:400, 0:400] = (0,0,0)

d1 = {}
d2 = {}
#cv2.imshow('result', img)
#cv2.imwrite('result.png', img)
