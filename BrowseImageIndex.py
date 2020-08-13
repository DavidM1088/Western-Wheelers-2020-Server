from tkinter import *
import tkinter as tk

class ImageIndexEdit:
    dir = '/Users/davidm/Library/Containers/com.david-murphy.Western-Wheelers-Quiz-Upload/Data/Documents/data'
    images = []
    descs = []
    index = 0
    root = tk.Tk()
    image_num = tk.StringVar()
    image_desc = tk.StringVar()

    def __init__(self):
        index_fle = open(self.dir + "/index.txt", "r")
        for line in index_fle:
            fields = line.split(', ')
            self.images.append(fields[0])
            self.descs.append(fields[2])
        index_fle.close()

    def show(self, num):
        img_file = self.dir + "/" + str(num) + ".png"
        self.img_in = tk.PhotoImage(file=img_file)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_in)

    def load_next(self):
        im = self.images[self.index]
        self.show(im)
        self.image_num.set(str(im))
        self.image_desc.set(self.descs[self.index])
        self.index += 1

    def load(self, num):
        #num = "100090"
        num = self.image_num.get()
        self.show(self.index, num)

    def delete(self):
        index_fle = open(self.dir + "/index.txt", "r")
        lines = []
        deleted = 0
        for line in index_fle:
            fields = line.split(', ')
            if fields[0] == self.image_num.get():
                deleted += 1
                continue
            lines.append(line)
        index_fle.close()
        print ("Deleted:", deleted)

        out_fle = open(self.dir + "/index.txt", "w")
        for line in lines:
            out_fle.write(line)
        out_fle.close()
        print("Wrote:", len(lines))

    def run(self):

        self.canvas = tk.Canvas(self.root, width = 800, height = 800)
        self.canvas.pack()

        #self.image_num_entry = Entry(root, width=10)
        tk.Entry(self.root, textvariable=self.image_num, font=('calibre', 10, 'normal')).pack()

        btn2 = Button(self.root, text="load next", command=self.load_next)
        btn2.pack()

        tk.Entry(self.root, textvariable=self.image_desc, font=('calibre', 10, 'normal')).pack()

        var = StringVar()
        var.set("----------------------")
        label = Label(self.root, textvariable=var).pack()

        btn1 = Button(self.root, text="load image num", command=self.load)
        btn1.pack()

        btn3 = Button(self.root, text="Delete image num", command=self.delete)
        btn3.pack()

        self.canvas.pack()
        self.root.mainloop()

ImageIndexEdit().run()
