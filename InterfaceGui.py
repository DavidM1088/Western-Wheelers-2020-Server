import os
import time
import tkinter as tk
from PIL import Image, ImageTk
import random
import numpy as np

class ImageProcess:
    clicks = 0
    top_left = ()
    btm_right = ()

    def __init__(self):
        pass

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

    def is_letter(self, img, r, c):
        r, g, b = img.get(c, r)
        bright = r + g + b
        if bright < 400:
            return False
        #ms = self.monochrome_score(img[r, c])
        monochrome = np.std([r,g,b])
        if monochrome > 2.0:
            return False
        return True

    def blank_out(self):
        # for x in range(self.top_left[0], self.btm_right[0]):
        #     for y in range(self.top_left[1], self.btm_right[1]):
        #         self.img1.put("#ffffff", (x, y))

        for r in range(self.top_left[1], self.btm_right[1]):
            for c in range(self.top_left[0], self.btm_right[0]):
                if self.is_letter(self.img_in, r, c):
                    self.img_out.put("#000000", (c, r))
                    tot_r = 0
                    tot_g = 0
                    tot_b = 0
                    cnt = 0
                    span = 20000
                    for c1 in range(40, span):
                        if not self.is_letter(self.img_in, r, c-c1):
                            red, g, b = self.img_in.get(c-c1, r)
                            tot_r += red
                            tot_g += g
                            tot_b += b
                            cnt += 1
                            if cnt > 3:
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
                    for cn in range(-span, 1):
                        #result[r + rn, c + cn] = avg
                        #image.put("#%02x%02x%02x" % (red, green, blue), (c+cn, r))
                        colr = "#%02x%02x%02x" % (tot_r, tot_g, tot_b)
                        self.img_out.put(colr, (c + cn, r))
                        #self.img_out.put("#%02x%02x%02x" % (0,0,0), (c + cn, r))
                        #self.img_out.put("#000000", (c+cn, r))

    def process_image(self):
        self.img_out = tk.PhotoImage(file=self.img_fle)
        w = self.img_out.width()
        #result = self.textExample.get("1.0", "end")
        #print(self.img1, w)
        self.blank_out()
        self.canvas.create_image(w + 10, 0, anchor=tk.NW, image=self.img_out)
        self.img_out.write('some_name.png', format='png')

    def print_event(self, event):
        position = "(x={}, y={})".format(event.x, event.y)
        print(event.type, "event", position)
        if self.clicks == 0:
            self.top_left = (event.x, event.y)
        else:
            self.btm_right = (event.x, event.y)
        self.clicks += 1
        if self.clicks == 2:
            self.process_image()

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

        btnRead = tk.Button(self.root, height=1, width=10, text="Read", command=self.process_image)
        btnRead.pack(side=tk.LEFT)
        self.frame.pack()
        self.root.mainloop()

proc = ImageProcess()
dir = '../../Desktop'
done = os.listdir(dir)
cnt = 0
while True:
    entries = os.listdir('../../Desktop')
    for e in entries:
        if e.find('1.png') < 0:
            continue
        nm = dir +'/'+e
        # if e in done:
        #     time.sleep(0.5)
        #     cnt += 1
        #     print ('wait..', cnt)
        #     continue

        proc.show(nm)
        done.append(e)
        break
        continue