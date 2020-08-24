import cv2
from math import sqrt
from scipy import spatial
import time
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import cv2
import urllib
import PIL
import requests
import tkinter as tk
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip



import tensorflow_hub as hub
import pandas as pd
import matplotlib.pyplot as plt 
import base64
from PIL import Image
import io
import math 
from math import sqrt
from tensorflow.keras.optimizers import Adam
from keras.models import load_model
from numpy import expand_dims
from keras.preprocessing.image import load_img
import pickle
from keras.preprocessing.image import img_to_array
from tensorflow.keras.optimizers import Adam



root = None
res = False


def cosineSim(a1,a2):
    result = 1 - spatial.distance.cosine(a1[0], a2[0])
    return result

l=[]
sec=0
frameRate = 0.5
frame_no=1
dict={}



model = load_model('model2.model')

f = open("type_lb.pickle","rb")

typeLB = pickle.loads(f.read())


f = open("color_lb.pickle","rb")
colorLB = pickle.loads(f.read())







def predict(path):
    image = cv2.imread(path)
    
    image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = img_to_array(image)
    samples = expand_dims(image, 0)
    res = model.predict(samples)

    return {'path':path,
    'type':typeLB.classes_[np.argmax(res[0][0])],
    'color':colorLB.classes_[np.argmax(res[1][0])],
    'timestamp':time}
    
    




def Algo_attribs(video_dict,query_list):

    result=[]
    for x in query_list:
        for y in video_dict:
            if(x['color']==y['color'] and x['type']==y['type']):
                result.append(y)

    return result
    






def Algo(video_dict,image_path,id_image,start_sec,end_sec):

    t1 = time.time()
  

    query_list=[]
    loc=os.path.join(r'SIH',str(id_image))
    os.mkdir(loc)
    #Query image
    count=1
    for x in image_path:
            file=Image.open(urllib.request.urlopen(x))
            file.save(loc+'/query_image'+str(count)+'.png')#print(loc+'\query_image.png')
            i1 = predict(loc+'/query_image'+str(count)+'.png')
            query_list.append(i1)
            count=count+1
    result=[]
    for x in query_list:
        for y in video_dict:
            if(x['color']==y['color'] and x['type']==y['type'] and (y['timestamp']>=start_sec and y['timestamp']<=end_sec) ):
                result.append(y)


    
    t2 = time.time()
    print("Query Time Taken to recognize Baggages "+str(t2-t1)+" sec")
    return result



def toggle():
    '''
    use
    t_btn.config('text')[-1]
    to get the present state of the toggle button
    '''
    global res
    if t_btn.config('text')[-1] == 'True':
        t_btn.config(text='False')
        res = False
    else:
        t_btn.config(text='True')
        res = True

def openWindow(path):
    global root
    root = tk.Tk()
    frame = Frame(root)
    frame.pack()
    t_btn = tk.Button(frame,text="True", width=12, command=toggle)
    btn_exit = tk.Button(frame,text = "Exit",width=12,command=exit)
    t_btn.grid(row=0,column=0)
    btn_exit.grid(row=0,column=1,padx=10,pady=10)
    img = PIL.ImageTk(PIL.Image.open(path))
    lab = Label(root,image = img)
    lab.pack(padx=10,pady=10) 
    root.mainloop()

def exit():
    global root
    root.destroy()
