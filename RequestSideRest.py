import requests,os,json

arr = os.listdir("dataa")
for aa in arr:
    files = {
        'file': open(f'dataa/{aa}', 'rb'),
    }
    files2 = {
        'file': open(f'dataa/{aa}', 'rb'),
    }

    VehicleTypeDetection = requests.post('http://localhost:5000/VehicleTypeDetection', files=files)
    VehicleTypeDetectionJson = json.loads(VehicleTypeDetection.text)
    print(VehicleTypeDetectionJson)
    ALPRI = requests.post('http://localhost:5000/ALPR', files=files2)
    ALPRJson = json.loads(ALPRI.text)
    print(ALPRJson)
    # break
