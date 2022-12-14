import json
from flask import jsonify
from matplotlib.font_manager import json_load
import requests
import base64
import os
from itertools import accumulate
import cv2
arr = os.listdir("dataa")
for aa in arr:
    with open(f"dataa/{aa}", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())

    stttt =  my_string.decode("utf-8")
    payload={"img":stttt}
    asd=requests.post(url="http://192.168.18.81:5000/VehicleTypeDetection/", json=payload)
    a2a = json.loads(asd.text)
    print(a2a)
    asd=requests.post(url="http://192.168.18.81:5000/ALPR/", json=payload)
    a2a = json.loads(asd.text)
    print(a2a)