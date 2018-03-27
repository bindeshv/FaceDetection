import json 
import cognitive_face as cf 

keys = None

#load the key from json file 
with open('keys.json') as data:
    keys = json.load(data)
    data.close()

#initialize the API keys and endpoint
cf.Key.set(keys["api_key"])
cf.BaseUrl.set(keys["api_endpoint"])

img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
result = cf.face.detect(img_url)
print(result)



