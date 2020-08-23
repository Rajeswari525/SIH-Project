import PIL.Image
import GUI_SIH
from tkinter.font import *
from tkinter import *
from tkinter import filedialog
import PIL.ImageTk


class App(Frame):
    def chg_image(self):
                # photo image
        self.img = PIL.ImageTk.PhotoImage(PIL.Image.open(self.l[self.num_page]))
        self.la.config(image=self.img, bg="#000000",
            width=self.img.width(), height=self.img.height())

  
    def seek_prev(self):
        self.num_page=self.num_page-1
        if self.num_page < 0:
            self.num_page = 0
       
        self.chg_image()
        self.num_page_tv.set("ID:"+str(self.num_page+1))

    def seek_next(self):
        self.num_page=self.num_page+1
        if self.num_page == len(self.l):
            self.num_page=self.num_page-1
        self.chg_image()
        self.num_page_tv.set("ID:"+str(self.num_page+1))
    
    def exit(self):
        self.master.destroy()
        GUI_SIH.Main()

    def __init__(self,l, master=None):
        Frame.__init__(self, master)
        self.master.title('Output')
        self.l=l

        self.num_page=0
        self.num_page_tv = StringVar()
        self.num_page_tv.set("ID:"+str(self.num_page+1))

        fram = Frame(self,padx=10,pady=10)
        
        Button(fram, text="Prev", command=self.seek_prev).pack(side=LEFT)
        Button(fram, text="Next", command=self.seek_next).pack(side=RIGHT)
        Button(fram, text="Exit", command=self.exit).pack()

        fram1 = Frame(self)
        fram1.pack()
        Label(fram1, textvariable=self.num_page_tv,fg="red",font=Font(fram1,weight="bold",size=10)).pack(side=LEFT)
        fram.pack(side=TOP, fill=BOTH)

        self.la = Label(self)
        self.la.pack()

        self.pack()
        self.chg_image()



