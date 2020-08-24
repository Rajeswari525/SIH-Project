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
from keras.models import load_model
from numpy import expand_dims
from keras.preprocessing.image import load_img
import pickle
from keras.preprocessing.image import img_to_array
from tensorflow.keras.optimizers import Adam
 
model = load_model('model.h5')


f = open("type_lb.pickle","rb")
typeLB = pickle.loads(f.read())


f = open("color_lb.pickle","rb")
colorLB = pickle.loads(f.read())


def predict(path,time):
    image = cv2.imread(path)
    
    image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = img_to_array(image)
    samples = expand_dims(image, 0)
    res = model.predict(samples)

    return {'path':path,
    'type':typeLB.classes_[np.argmax(res[0][0])],
    'color':colorLB.classes_[np.argmax(res[1][0])],
    'timestamp':time    
    }


import tensorflow_hub as hub
import pandas as pd
import matplotlib.pyplot as plt 
import base64
from PIL import Image
import io
import math 
from math import sqrt


root = None
res = False



l=[]
sec=0
frameRate = 0.5
frame_no=1
dict={}


def boxes(cap,detection_graph,tf_compat,categories,width, height,loc):
    sec,frameRate,frame_no,res = 0,0.5,1,[]
    x=cap.get(cv2.CAP_PROP_FPS)
    target = x//2
    ret,counter=True,0
    c = 0
    with detection_graph.as_default():
        with tf_compat.Session(graph=detection_graph) as sess:
            while ret:
                print(sec,c)
                if counter == target:
                    c+=1            
                    ret,image_np=cap.read()
                    if not ret:
                        break
                    counter = 0
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                    (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})
                    box = np.squeeze(boxes)
                    sc = np.squeeze(scores)
                    cl = np.squeeze(classes)
                    j=1
                    if(c==2):
                        sec+=1
                        c=0                   
                    for i in range(len(cl)):
                        if cl[i] in categories and sc[i] >= 0.30:
                            ymin = (int(box[i,0]*height))
                            xmin = (int(box[i,1]*width))
                            ymax = (int(box[i,2]*height))
                            xmax = (int(box[i,3]*width))
                            # print(len(box),len(sc),cl)
                            if (ymin == 0 and xmin==0 and ymax==0 and xmax==0):
                                break
                            crop_img = image_np[ymin:ymax, xmin:xmax]                 
                            s='i'+str(frame_no)+'_'+str(j)
                            s=os.path.join(loc,s+'.png')
                            cv2.imwrite(s, crop_img)
                            res.append({'path':s,'timestamp':sec})
                            j=j+1
                    print("Processing of Frame: "+str(frame_no) + " completed.")
                    frame_no=frame_no+1
                else :
                    ret = cap.grab()
                    counter += 1
    return res






def Algo(video_path):

    t1 = time.time()  
    length = len(os.listdir('SIH_Video'))
    loc=os.path.join(r'SIH_Video',str(length+1))
    os.mkdir(loc)
  
    #data related to Model     
    MODEL_NAME = 'faster_rcnn_inception_v2_coco_2018_01_28'    #model currently being used (ssd_inception_v2_coco_2017_11_17 )
    #MODEL_FILE = MODEL_NAME + '.tar.gz'     #the model should be downloaded using .tar.gz
    #DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'   #the model should be downloaded from here
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
    PATH_TO_LABELS = os.path.join('object_detection/data', 'mscoco_label_map.pbtxt')    #it contains labels present in coco data set
    
    #Load the video
    cap = cv2.VideoCapture(video_path)    #captures file from the path and stores it in cap 
    a,b = cap.read()
    print("Video Loaded Successfully.")
    capSize = (b.shape[1] , b.shape[0])
    
    #Model Download
    NUM_CLASSES = 90
    '''opener = urllib.request.URLopener()
    opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
    tar_file = tarfile.open(MODEL_FILE)
    for file in tar_file.getmembers():
        file_name = os.path.basename(file.name)
        if 'frozen_inference_graph.pb' in file_name:
            tar_file.extract(file, os.getcwd())'''
    
    #tensorflow graphs -->ding tensorflow graphs into the memory
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.compat.v2.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    
    label_map_util.tf = tf.compat.v1
    tf.gfile = tf.io.gfile
    
    # Encoding labels
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    
    #initializing variables
    j=1
    width, height = capSize
    categories = [27,31,33]
    ymin, ymax, xmin, xmax = -1,-1,-1,-1
    
    #capturing bags
    path_list=[]
    print("Successsfullly extracted bounding boxes of bags in each frame.")
    d1= boxes(cap,detection_graph,tf.compat.v1,categories,width, height,loc)


    d1 = [predict(x['path'],x['timestamp']) for x in d1 ]
    print(d1)
  
    
    t2 = time.time()
    print("Query Time Taken to recognize Baggages "+str(t2-t1)+" sec")
    return (d1,length+1)
