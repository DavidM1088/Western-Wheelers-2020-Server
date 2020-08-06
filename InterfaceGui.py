import os
from os import path
import time
import tkinter as tk
import random
import numpy as np
from datetime import datetime
from PIL import Image, ImageTk

class ImageProcess:
    clicks = None
    top_left = ()
    btm_right = ()

    def __init__(self):
        #self.dir = './data/files_out/'
        self.out_dir = '/Users/davidm/Library/Containers/com.david-murphy.Western-Wheelers-Quiz-Upload/Data/Documents/data'
        self.index_fle = None
        if not path.exists(self.out_dir+"/index.txt"):
            f = open(self.out_dir+"/index.txt", "w")
            f.write("")
            f.close()

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
        return diff < 50

    def blank_out(self, col_start, col_end, direction):
        # for x in range(self.top_left[0], self.btm_right[0]):
        #     for y in range(self.top_left[1], self.btm_right[1]):
        #         self.img1.put("#ffffff", (x, y))
        print ('start row, col:', self.top_left[1], self.top_left[0])
        for r in range(self.top_left[1], self.btm_right[1]):
            for c in range(col_start, col_end, direction):
                if self.is_letter(self.img_in, r, c):
                    #self.img_out.put("#000000", (c, r))
                    #continue
                    tot_r = 0
                    tot_g = 0
                    tot_b = 0
                    cnt = 0
                    span = 20000
                    for c1 in range(40, span):
                        if c1 > c :
                            raise Exception("no edge to letter, row, col:", r, c)
                        if not self.is_letter(self.img_in, r, c-(direction*c1)):
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
        h = self.img_out.height()
        mid = self.top_left[0] + (self.btm_right[0] - self.top_left[0]) // 2
        self.blank_out(self.top_left[0], mid, 1)
        self.blank_out(mid, self.btm_right[0], 1)
        self.canvas.create_image(w + 10, 0, anchor=tk.NW, image=self.img_out)
        #self.save()

    def print_event(self, event):
        if self.clicks is None:
            return
        position = "(x={}, y={})".format(event.x, event.y)
        print(event.type, "event", position, self.clicks)
        if self.clicks == 0:
            r,g,b = self.img_in.get(event.x, event.y)
            self.letr_colr = (r, g, b)
            self.log_text.set("Got letter color, click top left")
        if self.clicks == 1:
            self.top_left = (event.x, event.y)
            self.log_text.set("Got top left, click bottom right")
        if self.clicks == 2:
            self.btm_right = (event.x, event.y)
            self.log_text.set("Got bottom right")
            self.process_image()
        self.clicks += 1

    def save(self):
        num = len(os.listdir(self.out_dir))
        num += 100000
        dt = time.strftime('%Y\%m\%d')

        cords_lat = 0
        cords_long = 0
        if len(self.url.get()):
            coords = self.url.get().split("@")[1]
            if len(coords) > 0:
                cords_lat = coords.split(',')[0]
                cords_long = coords.split(',')[1]

        index_fle = open(self.out_dir + "/index.txt", "a")
        index_fle.write(str(num) + ', ' + dt + ', ' + self.desc.get() + ", " + str(cords_lat) + ", "+str(cords_long) + ", "+self.url.get() + "\n")
        index_fle.close()

        self.img_in.write('./data/files_in/' + str(num) + '.png', format='png')

        self.img_out.write("temp.png", format='png')
        w = self.img_out.width()
        h = self.img_out.height()

        m = 0.8
        img = Image.open('temp.png')
        img = img.resize((int(w * m), int(h * m)), Image.ANTIALIAS)
        img.save(self.out_dir + '/'  + str(num) + '.png')
        print("---- SAVED ----")
        self.root.destroy()

    def cancel(self):
        self.root.destroy()

    def show(self, img_file):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        #self.frame.pack()
        self.img_fle = img_file
        self.img_in = tk.PhotoImage(file=img_file)

        h = self.img_in.height()
        w = self.img_in.width()
        print(img_file, self.img_in.width(), self.img_in.height())
        self.canvas = tk.Canvas(self.root, width = 2*w+10, height = h)
        self.canvas.pack()
        self.canvas.create_image(0,0, anchor=tk.NW, image=self.img_in)
        self.canvas.bind("<Button-1>", self.print_event)

        self.url = tk.StringVar()
        self.url.set("")
        self.urk_entry = tk.Entry(self.root, textvariable=self.url, font=('calibre', 10, 'normal')).pack(ipadx=400)

        self.desc = tk.StringVar()
        self.desc.set("desc")
        self.desc_entry = tk.Entry(self.root, textvariable=self.desc, font = ('calibre', 10, 'normal')).pack()

        tk.Button(self.root, text="Start", command=self.start).pack()
        tk.Button(self.root, text="Save", command=self.save).pack()
        tk.Button(self.root, text="Cancel", command=self.cancel).pack()

        self.log_text = tk.StringVar()
        img_ratio = float(h) / float(w)
        self.log_text.set('Ratio: '+str(img_ratio)+ ', enter road name and then click start')
        self.log = tk.Label(self.root, textvariable=self.log_text).pack()

        # tk.Label(self.root, text="First Name").grid(row=0)
        # tk.Label(self.root, text="Last Name").grid(row=1)
        # e1 = tk.Entry(self.root)
        # e2 = tk.Entry(self.root)
        # e1.grid(row=0, column=1)
        # e2.grid(row=1, column=1)

        self.frame.pack()
        self.root.mainloop()
        print ("---- END ----")

proc = ImageProcess()

dir = '../../Desktop'
done = os.listdir(dir)
cnt = 0
while True:
    entries = os.listdir('../../Desktop')
    time.sleep(0.5)
    for e in entries:
        # if e.find('1.png') < 0:
        #     continue
        nm = dir +'/'+e
        if e in done:
            cnt += 1
            print ('wait..', cnt)
            continue

        proc.show(nm)
        done.append(e)
        #break
        continue