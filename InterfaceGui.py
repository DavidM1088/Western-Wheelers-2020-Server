import os
import time
import tkinter as tk
from PIL import Image, ImageTk

def print_event(event):
        position = "(x={}, y={})".format(event.x, event.y)
        print(event.type, "event", position)


def show(img_file):
    root = tk.Tk()
    frame = tk.Frame(root)

    canvas = tk.Canvas(root, width = 300, height = 300)
    canvas.pack()
    canvas.bind("<Button-1>", print_event)
    canvas.bind("<B1-Motion>", print_event)
    img = tk.PhotoImage(file=img_file)
    canvas.create_image(20,20, anchor=tk.NW, image=img)

    textExample = tk.Text(root, height=10)
    textExample.pack()

    textExample = tk.Text(root, height=10)
    textExample.pack()

    def getTextInput():
        result = textExample.get("1.0", "end")
        print(result)
        im1 = Image.open(img_file)
        px = im1.load()
        print(px[4, 4])
        px[4, 4] = (0, 0, 0)
        print(px[4, 4])
        canvas.create_image(20, 20, anchor=tk.SW, image=img)

    btnRead = tk.Button(root, height=1, width=10, text="Read", command=getTextInput)
    btnRead.pack(side=tk.LEFT)
    frame.pack()
    root.mainloop()

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

        print (nm)
        show(nm)
        done.append(e)
        break
        continue