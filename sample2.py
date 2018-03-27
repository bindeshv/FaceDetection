import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json


face_api_key = "2ddfcea20c8b49a3a60501e26c899912"
face_api_endpoint = "https://southcentralus.api.cognitive.microsoft.com/face/v1.0/detect"
face_to_detect = None

has_exception = False 

headers = {
    'Content-Type': 'Application/Octet-Stream',
    'Ocp-Apim-Subscription-Key': face_api_key
}

try: 
    with open('mypic.jpg', 'rb') as image:
        img = image.read()
        face_to_detect = bytearray(img)
        print("image reading done!")
        #print(face_to_detect)
except Exception as ex:
    print("exception in reading image bytes {0}".format(ex.args))
    has_exception = True

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}


try:

    print("posting image")
    params = urllib.parse.urlencode(params)
    print(params)
    conn = http.client.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
    conn.request("POST",face_api_endpoint+"?%s" % params,body=face_to_detect, headers=headers)
    resp = conn.getresponse()

    if resp.status == 200:
        resp_data = resp.read()
        print(resp_data)
    else:
        print("error in response: {0} {1}".format(resp.status, resp.reason))

    conn.close() 
    

except Exception as ex:
    print("error in posting {0}".format(ex.args))