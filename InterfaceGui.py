import math
import os
import time
import tkinter as tk
from PIL import Image, ImageTk
import random
import numpy as np

class ImageProcess:
    clicks = None
    top_left = ()
    btm_right = ()

    def __init__(self):
        pass

    def start(self):
        self.clicks = 0
        self.log_text.set('1) Click on letter, 2) click top left, 3) click bottom right')

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
    row_avg = []

    def is_letter_old(self, img, r, c):
        r, g, b = img.get(c, r)
        bright = r + g + b
        if bright < 400:
            return False
        #ms = self.monochrome_score(img[r, c])
        monochrome = np.std([r,g,b])
        if monochrome > 2.0:
            return False
        return True

    def is_letter(self, img, r, c):
        r, g, b = img.get(c, r)
        diff = abs(r - self.letr_colr[0]) + abs(g - self.letr_colr[1]) + abs(b - self.letr_colr[2])
        return diff < 40

    def blank_out(self):
        # for x in range(self.top_left[0], self.btm_right[0]):
        #     for y in range(self.top_left[1], self.btm_right[1]):
        #         self.img1.put("#ffffff", (x, y))
        print ('start row, col:', self.top_left[1], self.top_left[0])
        for r in range(self.top_left[1], self.btm_right[1]):
            for c in range(self.top_left[0], self.btm_right[0]):
                if self.is_letter(self.img_in, r, c):
                    #self.img_out.put("#000000", (c, r))
                    #continue
                    tot_r = 0
                    tot_g = 0
                    tot_b = 0
                    cnt = 0
                    span = 20000
                    for c1 in range(40, span):
                        if c1 > c:
                            raise Exception("no edge to letter, row, col:", r, c)
                        if not self.is_letter(self.img_in, r, c-c1):
                            red, g, b = self.img_in.get(c-c1, r)
                            tot_r += red
                            tot_g += g
                            tot_b += b
                            cnt += 1
                            if cnt > 16:
                                break
                    if cnt > 0:
                        tot_r = tot_r // cnt
                        tot_g = tot_g // cnt
                        tot_b = tot_b // cnt

                    max = 6
                    r1 = random.randint(-max, max)
                    # r2 = random.randint(-max, max)
                    # r3 = random.randint(-max, max)
                    tot_r += r1
                    tot_g += r1
                    tot_b += r1

                    span = 10
                    #span += random.randint(0, 2)
                    #for rn in range(-span, span):
                    for cn in range(-span, span):
                        if tot_r > 255: tot_r = 255
                        if tot_g > 255: tot_g = 255
                        if tot_b > 255: tot_b = 255
                        colr = "#%02x%02x%02x" % (tot_r, tot_g, tot_b)
                        self.img_out.put(colr, (c + cn, r))

    def process_image(self):
        self.img_out = tk.PhotoImage(file=self.img_fle)
        w = self.img_out.width()
        #result = self.textExample.get("1.0", "end")
        #print(self.img1, w)
        self.blank_out()
        self.canvas.create_image(w + 10, 0, anchor=tk.NW, image=self.img_out)

        dir = './data/files_out'
        num  = len(os.listdir(dir))
        num += 100000
        self.img_in.write('./data/files_in/'+str(num)+'.png', format='png')
        self.img_out.write('./data/files_out/'+str(num)+'.png', format='png')
        print("---- SAVED ----")

    def print_event(self, event):
        if self.clicks is None:
            return
        position = "(x={}, y={})".format(event.x, event.y)
        print(event.type, "event", position, self.clicks)
        if self.clicks == 0:
            r,g,b = self.img_in.get(event.x, event.y)
            self.letr_colr = (r, g, b)
            self.log_text.set("Got letter color")
        if self.clicks == 1:
            self.top_left = (event.x, event.y)
            self.log_text.set("Got top left")
        if self.clicks == 2:
            self.btm_right = (event.x, event.y)
            self.log_text.set("Got bottom right")
            self.process_image()
        self.clicks += 1

    def show(self, img_file):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.img_fle = img_file
        self.img_in = tk.PhotoImage(file=img_file)

        h = self.img_in.height()
        w = self.img_in.width()
        print(img_file, self.img_in.width(), self.img_in.height())
        self.canvas = tk.Canvas(self.root, width = 2*w+10, height = h)
        self.canvas.pack()

        self.canvas.create_image(0,0, anchor=tk.NW, image=self.img_in)
        #textExample = tk.Text(root, height=10)
        #textExample.pack()

        self.canvas.bind("<Button-1>", self.print_event)
        #canvas.bind("<B1-Motion>", print_event)

        #btnRead = tk.Button(self.root, height=1, width=10, text="Read", command=self.process_image)
        #btnRead.pack(side=tk.LEFT)

        self.log_text = tk.StringVar()
        self.log_text.set('Click start')
        self.log = tk.Label(self.root, textvariable=self.log_text).pack()

        tk.Button(self.root, text="Start", command=self.start).pack()
        tk.Button(self.root, text="Quit", command=self.root.destroy).pack()

        self.frame.pack()
        self.root.mainloop()
        print ("---- END ----")

dir = '../../Desktop'
done = os.listdir(dir)
cnt = 0
while True:
    entries = os.listdir('../../Desktop')
    for e in entries:
        # if e.find('1.png') < 0:
        #     continue
        nm = dir +'/'+e
        if e in done:
            time.sleep(0.5)
            cnt += 1
            print ('wait..', cnt)
            continue
        proc = ImageProcess()
        proc.show(nm)
        done.append(e)
        break
        continue