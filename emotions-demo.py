import json
#from IPython.display import HTML
import requests

keys = None

#load the key from json file 
with open('keys.json') as data:
    keys = json.load(data)
    data.close()
    

image_url = 'https://how-old.net/Images/faces2/main007.jpg'
headers = { 'Ocp-Apim-Subscription-Key': keys['api_key'] }
face_api_url = 'https://southcentralus.api.cognitive.microsoft.com/face/v1.0/detect' #keys['api_endpoint']

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}


response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
faces = response.json()