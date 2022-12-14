#!/usr/bin/python
# coding: utf-8
import torch
import cv2
import time
# import pytesseract
import re
import numpy as np
import easyocr,json
import glob
import cv2 as cv
import base64
from flask import Flask, flash, request, redirect, url_for,jsonify
global model
global model2
model =  torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt',force_reload=True) 
model2 =  torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt',force_reload=True) 
model.conf = 0.35  # NMS confidence threshold
# model.iou = 0.45  # NMS IoU threshold
    #   agnostic = False  # NMS class-agnostic
    #   multi_label = False  # NMS multiple labels per box
model.classes = [2,3,5,7]  # (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
    #   max_det = 1000  # maximum number of detections per image
    #   amp = False  # Automatic Mixed Precision (AMP) inference
application = Flask(__name__)
@application.route('/')
def entry_point():
    return " This Vehicle Identification API Status -->> Active "

@application.route('/VehicleTypeDetection/', methods=['POST'])
def VehicleTypeDetection():
    if request.method == 'POST':
        global model
        arggg = (request.json)
        eencodee = arggg['img'].encode("utf-8")
        ff = base64.decodebytes(eencodee)
        jpg_as_np = np.frombuffer(ff, dtype=np.uint8)
        frame = cv2.imdecode(jpg_as_np, flags=1) 
        results = model(frame)
        labels = (results.pandas().xyxy[0].name) 
        n = len(labels)
        laibels = []
        for i in range(n):
            lla = labels[i]
            laibels.append(lla)        
        return json.dumps({'Vehicles list':laibels, 'Status' : 1})


@application.route('/ALPR/', methods=['POST'])
def ALPR():
    if request.method == 'POST':
        global model2
        arggg = (request.json)
        eencodee = arggg['img'].encode("utf-8")
        ff = base64.decodebytes(eencodee)
        jpg_as_np = np.frombuffer(ff, dtype=np.uint8)
        frame = cv2.imdecode(jpg_as_np, flags=1) 
        results = model2(frame)
        labels = (results.pandas().xyxy[0].name) 
        n = len(labels)
        laibels = []
        for i in range(n):
            lla = labels[i]
            laibels.append(lla)        
        return json.dumps({'Licence Plate list':laibels, 'Status' : 1})



if __name__ == "__main__" :
    application.run(host='0.0.0.0')