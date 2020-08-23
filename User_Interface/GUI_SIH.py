
from tkinter import *
from tkinter import ttk
import  tkinter.messagebox
import app,output,Algo_queryimg
from tkinter.font import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk,Image
import PIL.ImageTk,PIL.Image
import urllib,requests
import Algo_video


l = []
output_image = None
output_image_id = 0
prev_image_button=None
next_image_button=None
output_frame=None
root=None


class App(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.hourstr=StringVar(self,'00')
        self.hour = Spinbox(self,from_=0,to=23,wrap=True,textvariable=self.hourstr,width=2,state="readonly")
        self.minstr=StringVar(self,'00')
        self.minstr.trace("w",self.trace_var)
        self.last_value = ""
        self.min = Spinbox(self,from_=0,to=59,wrap=True,textvariable=self.minstr,width=2,state="readonly")
        self.hour.grid()
        self.min.grid(row=0,column=1)
        

    def trace_var(self,*args):
        if self.last_value == "59" and self.minstr.get() == "0":
            self.hourstr.set(int(self.hourstr.get())+1 if self.hourstr.get() !="23" else 0)
        self.last_value = self.minstr.get()



class Main:
 
    def __init__(self):

        self.root = Tk()
        self.root.geometry('800x800')
        self.root.title('Baggage Detector System')
       
        self.video_footage_path=''
        self.id_image_txt = StringVar()
        
        rows = 0
        while rows<1000:
            self.root.rowconfigure(rows, weight=2)
            self.root.columnconfigure(rows, weight=2)
            rows+=1

        self.title = Label(self.root,fg="red",padx=20,pady=20,text='Baggage Detector System',font=Font(self.root,weight="bold",size=15))
        self.title.pack(fill=X)


        self.videoFrame = LabelFrame(self.root, text='Upload video',padx=10,pady=10,width=50,height=50,font=Font(self.root,weight="bold",size=10),fg="red")
        self.videoFrame.pack()

        self.videoButton = Button(self.videoFrame,text="Upload CCTV Footage",command=self.handleVideoUpload)
        self.videoButton.pack()

        self.frame = LabelFrame(self.root, text='Baggage Detection',padx=10,pady=10,width=50,height=50,font=Font(self.root,weight="bold",size=10),fg="red")
        self.frame.pack()
        self.BaggageFrame = Frame(self.frame)
        self.BaggageFrame.grid(row=1,column=0,padx=10,pady=10,columnspan=3)

        Label(self.BaggageFrame,text="Create new record:").grid(row=1,column=0,padx=2,pady=2)

        self.upload_image = Button(self.BaggageFrame, text = ' Upload Image',command=self.UploadAction)
        self.upload_image.grid(row = 1, column = 1, sticky = W,padx=5,pady=5)

        self.add_image_to_existing_record_id = StringVar()
        Label(self.BaggageFrame,text="Enter Record id:").grid(row=2,column=0,padx=2,pady=2)

        self.add_image_to_existing_record_entry = Entry(self.BaggageFrame,textvariable=self.add_image_to_existing_record_id)
        self.add_image_to_existing_record_entry.grid(row=2,column=1,padx=2,pady=2)

        self.BaggageFrame1 = Frame(self.BaggageFrame)
        self.BaggageFrame1.grid(row=3,column=0,columnspan=2,padx=5,pady=5)

        self.add_image_to_existing_record_button = Button(self.BaggageFrame1, text = 'Add image to an existing record',padx=5,pady=5,command=self.addImageToExistingRecord)
        self.add_image_to_existing_record_button.pack()

        self.classify_label = Label(self.frame,text="Classify Images",padx=10,pady=10,font=Font(self.frame,weight="bold",size=10))
        self.classify_label.grid(row=3,column=0)

      
        self.classify_image_label = Label(self.frame,text="Enter Image Id:",font=Font(self.frame,size=10,weight="bold"))
        self.classify_image_label.grid(row=4,column=0,padx=5,pady=5)

        self.id_image = Entry(self.frame,textvariable=self.id_image_txt)
        
        self.id_image.grid(row=4,column=1,padx=5,pady=5)
        

        self.frameTimer = Frame(self.frame)
        self.frameTimer.grid(row=6,column=0,columnspan=5)

        Label(self.frameTimer,text="Start Time:").grid(row=0,column=0)

        self.startTime = App(self.frameTimer)
        self.startTime.grid(row=0,column=1,padx=5,pady=5)
        print(self.startTime.hourstr.get(),self.startTime.minstr.get())

        Label(self.frameTimer,text="End Time:").grid(row=0,column=2)
        self.endTime = App(self.frameTimer)
        self.endTime.grid(row=0,column=3,padx=5,pady=5)
        print(self.endTime.hourstr.get(),self.endTime.minstr.get())

        self.classify_video_label = Label(self.frame,text="Enter Video ID",font=Font(self.frame,size=10,weight="bold"))
        self.classify_video_label.grid(row=5,column=0,padx=5,pady=5)

        self.video_record_id = StringVar()
        

        self.video_entry = Entry(self.frame, textvariable=self.video_record_id)
        self.video_entry.grid(row = 5, column = 1, sticky = W,padx=5,pady=5)
        

        

        status_container = Frame(self.frame)

        status_container.grid(row=7,columnspan=3,rowspan=3)  
        Button(status_container, text = 'Classify',command=self.classify).pack()
      

        self.frame1 = LabelFrame(self.root, text='Attribute Based Baggage Generation',padx=10,pady=10, width=50,height=50,font=Font(self.root,weight="bold",size=10),fg="red")
        self.frame11 = Frame(self.frame1,padx=10,pady=10)
        self.frame11.pack()

        self.colors=['grey','red','violet']
        self.types=['backpack','trolley']
        self.companies=['hp','magnum']
        self.views=['front','back','side']
        self.color_var = StringVar(self.frame1)
        self.color_var.set(self.colors[0])
        self.types_var = StringVar(self.frame1)
        self.types_var.set(self.types[0])
        self.companies_var = StringVar(self.frame1)
        self.companies_var.set(self.companies[0])
        self.views_var = StringVar(self.frame)
        self.views_var.set(self.views[0])

        Label(self.root,text='',padx=5,pady=5).pack()

        Label(self.frame11,text="Select Attributes",padx=5,pady=5,font=Font(self.frame11,weight="bold",size=10)).grid(row=0,column=0,columnspan=3)
        Label(self.frame11,text="Color:").grid(row=1,column=1)
        self.colors_drop = OptionMenu(self.frame11,self.color_var, *self.colors)
        self.colors_drop.grid(row=1,column=2)
        Label(self.frame11,text="Type:").grid(row=1,column=3)
        self.types_drop = OptionMenu(self.frame11,self.types_var,*self.types)
        self.types_drop.grid(row=1,column=4)
        # Label(self.frame11,text="Company:").grid(row=1,column=5)
        # self.companies_drop = OptionMenu(self.frame11,self.companies_var,*self.companies)
        # self.companies_drop.grid(row=1,column=6)
        

      
        self.frame12 = Frame(self.frame1,padx=5,pady=5)
        self.frame12.pack()

        self.classify_video_label_attribs = Label(self.frame12,text="Enter Video ID",font=Font(self.frame,size=10,weight="bold"))
        self.classify_video_label_attribs.grid(row=5,column=0,padx=5,pady=5)

        self.video_record_id_attribs = StringVar()
        

        self.video_entry_attribs = Entry(self.frame12, textvariable=self.video_record_id_attribs)
        self.video_entry_attribs.grid(row = 5, column = 1, sticky = W,padx=5,pady=5)

        # self.frame12Timer = Frame(self.frame12)
        # self.frame12Timer.grid(row=6,column=0,columnspan=4,rowspan=1)
        # Label(self.frame12Timer,text="Start Time:").grid(row=0,column=0)

        # self.startTime12 = App(self.frameTimer)
        # self.startTime12.grid(row=0,column=1,padx=5,pady=5)
        
        # print(self.startTime12.hourstr.get(),self.startTime12.minstr.get())

        # Label(self.frame12Timer,text="End Time:").grid(row=0,column=2)
        # self.endTime12 = App(self.frame12Timer)
        # self.endTime12.grid(row=0,column=3,padx=5,pady=5)
        # print(self.endTime12.hourstr.get(),self.endTime12.minstr.get())
        
        
        self.img_create_record_button = Button(self.frame1,text="classify",padx=5,pady=5,command=self.classify_attribs)
        self.img_create_record_button.pack()


        self.processing_label = Label(self.frame1,fg='red')
        self.processing_label.pack()

        self.frame1.pack()

        self.root.mainloop()

    def classify_attribs(self):
        # start_sec = int(self.startTime.hourstr.get())*60*60 + int(self.startTime.minstr.get())*60
        # end_sec = int(self.endTime.hourstr.get())*60*60 + int(self.endTime.minstr.get())*60
        video_id = self.video_record_id_attribs.get()
        if video_id == '':
            messagebox.showinfo("Status","You have not given proper input")
        else:
            video_data = app.get_Video_details(video_id)

        query = {'color':self.color_var.get(),'type':self.types_var.get()}
        res = Algo_queryimg.Algo_attribs(video_data,[query])
        l = res
        print(l)
        if(len(l)==0):
            messagebox.showinfo("Status","Sorry no bag found that suits your input.")
            return
        self.root.destroy()
        x=output.App(l,Tk())
        x.mainloop()


    def create_record_attribs(self):
     
        print(self.attrib_based_image_url)
        res = app.insertURLDB(self.attrib_based_image_url)
        messagebox.showinfo("Status",'Your Record id is '+str(res))
            

    def addImageToExistingRecord(self):
        self.add_image_to_existing_record_button['state']=DISABLED
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        if filename != '':
            res = app.updateImageDB(self.add_image_to_existing_record_id.get(),filename)
            if res == '':
                messagebox.showinfo("Error","No Record found with id: "+str(self.add_image_to_existing_record_id.get()))
            else:
                messagebox.showinfo("Status","Image added to record: "+str(self.add_image_to_existing_record_id.get()))
          
        else:
            messagebox.showinfo("Error","Image not selected")
        self.add_image_to_existing_record_button['state']=NORMAL
        self.add_image_to_existing_record_id.set('')



    def fun(self):
        
        for i in self.attrib_based_image_url:
            img = PIL.Image.open(urllib.request.urlopen(i))
            img.show()
             

    def handleVideoUploadAttribs(self):
        self.video_button_attribs['state']=ACTIVE
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        self.video_footage_path_attribs=filename
        if(filename != ''):
            pass
        else:
            messagebox.showinfo("Error","Video not selected")

      
    def attribute_getimage_handler(self):
        print(self.companies_var.get(),self.types_var.get(),self.views_var.get(),self.color_var.get())
        self.attrib_based_image_url = app.get_image_attribs(self.color_var.get(),self.types_var.get(),self.companies_var.get())
        if len(self.attrib_based_image_url) != 0:
            
            self.processing_label['text']='Found Image with required Attributes'
            self.attrib_img = self.attrib_based_image_url
            self.img_show_button['state']='normal'
            self.img_create_record_button['state']='normal'
        else:
            self.processing_label['text']="No Image found with required Attributes"
            


    




    def classify(self):
        id_image = self.id_image_txt.get()
        video_id = self.video_record_id.get()
        
        start_sec = int(self.startTime.hourstr.get())*60*60 + int(self.startTime.minstr.get())*60
        end_sec = int(self.endTime.hourstr.get())*60*60 + int(self.endTime.minstr.get())*60
        if id_image == '' or video_id == '':
            messagebox.showinfo("Status","You have not given proper input")
        else:
            image_url = app.getImageFromDB(id_image)
            video_data = app.get_Video_details(video_id)

            if len(image_url)==0:
                messagebox.showinfo("Error","No Record found with Id: "+str(id_image))
            else:
                print(image_url)
                print(len(image_url))
                #GR you need to 
                path_list=Algo_queryimg.Algo(video_data,image_url,id_image,start_sec,end_sec)
                global l
                l = path_list
                if(len(l)==0):
                    messagebox.showinfo("Status","Sorry no bag found that suits your input.")
                    

                    return
                self.root.destroy()
                x=output.App(l,Tk())
                x.mainloop()
                l_urls=[]
                for i in l:
                    self.res_output = app.outputsToDB(id_image,i)
                    l_urls.append(self.res_output)
            
               
               
               
               



    def handleVideoUpload(self):
        self.videoButton['state']=ACTIVE
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        self.video_footage_path=filename
        if(filename != ''):
            self.videoButton['state']=DISABLED
            res,id = Algo_video.Algo(filename)
            print("Returned value",res)
            app.store_video_boxes(res,id)
            messagebox.showinfo("Staus","Video ID:"+str(id))
            self.videoButton['state']=NORMAL



        else:
            messagebox.showinfo("Error","Video not selected")
        


    def handleImageUpload(self,path):
        try:
            self.upload_image['state']=DISABLED
            id_image = app.insertImageDB(path)
            print(id_image)
            messagebox.showinfo("Image Uploaded","Image uploaded with id as"+str(id_image))
            self.upload_image['state']=NORMAL
        except:

            messagebox.showerror("Error occured")

    def UploadAction(self,event=None):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        if filename!='':
            self.handleImageUpload(filename)
        else:
            messagebox.showinfo("Error","Image not selected")



   

        

    






if __name__ == '__main__':

    

   ma = Main()



