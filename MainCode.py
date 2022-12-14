from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug
import cv2 , json
import numpy as np
import torch
import io
global model
global model2
model =  torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt',force_reload=True) 
model2 =  torch.hub.load('ultralytics/yolov5', 'custom', path='best_small.pt',force_reload=True) 
model.conf = 0.35  
model.classes = [2,3,5,7]  


app = Flask(__name__)
api = Api(app)
upload_parser = reqparse.RequestParser(bundle_errors=True)
upload_parser.add_argument(
    'file',
    required=True,
    type=werkzeug.datastructures.FileStorage,
    location='files'
)

class VehicleTypeDetection(Resource):
    def post(self):
        global model
        args = upload_parser.parse_args()
        image = args.file
        in_memory_file = io.BytesIO()
        image.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        frame = cv2.imdecode(data, color_image_flag)
        results = model(frame)
        labels = (results.pandas().xyxy[0].name) 
        n = len(labels)
        laibels = []
        for i in range(n):
            lla = labels[i]
            laibels.append(lla)        
        return json.dumps({'Vehicles list':laibels, 'Status' : 1})

class ALPR(Resource):
    def post(self):
        global model2
        args = upload_parser.parse_args()
        image1 = args.file
        in_memory_file = io.BytesIO()
        image1.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        frame = cv2.imdecode(data, color_image_flag)
        results = model2(frame)
        labels = (results.pandas().xyxy[0].name) 
        n = len(labels)
        laibels = []
        for i in range(n):
            lla = labels[i]
            laibels.append(lla)        
        return json.dumps({'Licence Plate list':laibels, 'Status' : 1})

api.add_resource(ALPR, '/ALPR')
api.add_resource(VehicleTypeDetection, '/VehicleTypeDetection')

if __name__ == '__main__':
    app.run()