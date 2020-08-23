#!/usr/bin/env python
# coding: utf-8

# In[1]:




# In[2]:


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


# In[3]:


import tensorflow_hub as hub
import pandas as pd
import matplotlib.pyplot as plt 
import base64
from PIL import Image
import io
import math 
from math import sqrt


# In[4]:


global embed
embed = hub.KerasLayer(os.getcwd())
print(os.getcwd())


# In[5]:


class TensorVector(object):

    def __init__(self, FileName=None):
        self.FileName = FileName

    def process(self):

        img = tf.io.read_file(self.FileName)
        img = tf.io.decode_jpeg(img, channels=3)
        img = tf.image.resize_with_pad(img, 224, 224)
        img = tf.image.convert_image_dtype(img,tf.float32)[tf.newaxis, ...]
        features = embed(img)
        feature_set = np.squeeze(features)
        return list(feature_set)


# In[6]:


def convertBase64(FileName):
    """
    Return the Numpy array for a image 
    """
    with open(FileName, "rb") as f:
        data = f.read()
        
    res = base64.b64encode(data)
    
    base64data = res.decode("UTF-8")
    
    imgdata = base64.b64decode(base64data)
    image = Image.open(io.BytesIO(imgdata))
    
    return np.array(image)


# In[7]:


def cosineSim(a1,a2):
    sum = 0
    suma1 = 0
    sumb1 = 0
    for i,j in zip(a1, a2):
        suma1 += i * i
        sumb1 += j*j
        sum += i*j
    cosine_sim = sum / ((sqrt(suma1))*(sqrt(sumb1)))
    return cosine_sim


# In[8]:


l=[]
sec=0
frameRate = 0.5
frame_no=1
dict={}


# In[9]:


def boxes(cap,detection_graph,tf_compat,categories,width, height,loc):
    global l,sec,frameRate,frame_no,dict
    x=cap.get(cv2.CAP_PROP_FPS)
    target = x//2
    ret,counter=True,0
    with detection_graph.as_default():
        with tf_compat.Session(graph=detection_graph) as sess:
            while ret:
                if counter == target:
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
                    for i in range(len(cl)):
                        if cl[i] in categories and sc[i] >= 0.10:
                            ymin = (int(box[i,0]*height))
                            xmin = (int(box[i,1]*width))
                            ymax = (int(box[i,2]*height))
                            xmax = (int(box[i,3]*width))
                            # print(len(box),len(sc),cl)
                            if (ymin == 0 and xmin==0 and ymax==0 and xmax==0):
                                break
                            crop_img = image_np[ymin:ymax, xmin:xmax]
                            p=[]
                            p.append(list(np.squeeze(boxes)[i]))
                            p.append(classes[0][i])
                            p.append(scores[0][i])
                            s='i'+str(frame_no)+str(j)
                            dict[s]=p
                            cv2.imwrite(os.path.join(loc,s+'.png'), crop_img)
                            l.append(s+'.png')
                            j=j+1
                    print("Next Frame ",frame_no)
                    cv2.imwrite(os.path.join(loc,'f'+str(frame_no)+ '.png'), image_np)
                    frame_no=frame_no+1
                else :
                    ret = cap.grab()
                    counter += 1


# In[30]:


def fun(path,query_list,loc):
    for x in query_list:
        #q=convertBase64(os.path.join(loc,path))
        obj1=TensorVector(os.path.join(loc,path))
        vec = obj1.process()
        if(cosineSim(x,vec) >= 0.70):
            return 1
    return 0


# In[31]:


def Algo(video_path,image_path,id_image):
    query_list=[]
    loc=os.path.join(r'C:\Users\rajic\OneDrive\Attachments\Desktop\SIH',str(id_image))
    os.mkdir(loc)
    #Query image
    count=1
    for x in image_path:
            file=Image.open(urllib.request.urlopen(x))
            file.save(loc+'\query_image'+str(count)+'.png')#print(loc+'\query_image.png')
            #q=convertBase64(os.path.join(loc,'query_image.png'))
            obj=TensorVector(loc+'\query_image'+str(count)+'.png')
            query = obj.process()
            query_list.append(query)
            count=count+1
    
    #data related to Model     
    MODEL_NAME = 'faster_rcnn_inception_v2_coco_2018_01_28'    #model currently being used (ssd_inception_v2_coco_2017_11_17 )
    #MODEL_FILE = MODEL_NAME + '.tar.gz'     #the model should be downloaded using .tar.gz
    #DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'   #the model should be downloaded from here
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
    PATH_TO_LABELS = os.path.join('object_detection/data', 'mscoco_label_map.pbtxt')    #it contains labels present in coco data set
    
    #Load the video
    cap = cv2.VideoCapture(video_path)    #captures file from the path and stores it in cap 
    a,b = cap.read()
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
    #tensorflow graphs
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
    boxes(cap,detection_graph,tf.compat.v1,categories,width, height,loc)
    for x in l:
        sim=fun(x,query_list,loc)
        print(sim)
        if(sim):
            s=x[1]
            s1=x[0:-4]
            img = cv2.imread(os.path.join(loc,'f'+s+ '.png'))
            bx = np.reshape(dict[s1][0],(1,4))
            cs =np.array([dict[s1][1]])
            sci = np.array([dict[s1][2]])
            vis_util.visualize_boxes_and_labels_on_image_array(
                img,
            bx,
            cs.astype(np.int32),
            sci,
            category_index,
            use_normalized_coordinates=True,
            line_thickness=2)
            path_list.append(os.path.join(loc,'final'+s+ '.png'))
            cv2.imwrite(os.path.join(loc,'final'+s+ '.png'), img)
    return path_list





