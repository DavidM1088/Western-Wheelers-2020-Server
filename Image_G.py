import cv2
import numpy as np

class Image_G:
    light_threshold = 3 * 230
    dark_threshold = 3 * 180
    img = None

    def __init__(self, id):
        self.id = id
        file = 'images/'+id+'.png'
        self.img = cv2.imread(file)
        self.rows, self.cols, colors = self.img.shape
        self.row_edge = self.rows // 20
        self.row_start = self.row_edge
        self.row_end = self.rows - self.row_edge
        self.col_edge = self.cols // 20
        self.col_start = self.col_edge
        self.col_end = self.cols - self.col_edge

    def get_score(self, pix):
        white = 0
        for i in range(3):
            white += pix[i]
        return white

    def get_diff(self, p1, p2):
        diff = 0
        for i in range(3):
            diff = abs(p2[i] - p1[i])
        return diff

    def is_same(self, p1, p2):
        for i in range(3):
            if p1[i] != p2[i]:
                return False
        return True

    def monochrome_score(self, pix):
        score = np.std(pix)
        # score = abs(pix[1] - pix[0])
        # #print(p[0], p[1], p[2])
        # x = pix[2]
        # y = pix[1]
        # x = x - pix[1]
        # score += x
        # score += abs(p[2] - p[0])
        return score

    def process(self):
        for r in range (self.row_start, self.row_end):
            same_cnt = 0
            same_start = None
            last = None
            if (r %200 == 0):
                print ("row:"+str(r))

            c = self.col_start
            while c < self.col_end:
                if not last is None:
                    s1 = self.get_score(self.img[r, c])
                    s2 = self.get_score(last)
                    if abs (s1 - s2) < 19 and self.monochrome_score(self.img[r, c]) < 3:
                        #if str(img[r, c]) == str(last):
                        same_cnt += 1
                    else:
                        same_start = c
                        same_cnt = 0
                last = self.img[r, c]

                dark = 0

                if same_cnt > 4:
                    #print ("found run")
                    val = self.img[r, c-same_cnt-38]
                    right = 10;
                    left = 10;
                    if same_start is not None:
                        for cx in range(same_start-left, c+right):
                            if cx < self.cols:
                                self.img[r, cx] = val #(0,127,0) #val
                                #pass
                    c += right+1
                    same_cnt = 0
                    same_start = 0
                    same_start = None

                else:
                    c += 1


    def save(self):
        scale_percent = 60  # percent of original size
        width = int(self.img.shape[1] * scale_percent / 100)
        height = int(self.img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized = cv2.resize(self.img, dim) #, interpolation=cv2.INTER_AREA)
        self.saved_file = 'images/output/'+self.id+'.png'
        cv2.imwrite(self.saved_file, resized)