import cognitive_face as cf
import urllib,os
#from urllib import request 
#from cf import util 



face_api_key = "2ddfcea20c8b49a3a60501e26c899912"
face_api_endpoint = "https://southcentralus.api.cognitive.microsoft.com/face/v1.0/"
face_to_detect = None

cf.Key.set(face_api_key)
cf.BaseUrl.set(face_api_endpoint)

has_exception = False

#read image as binary 
# try: 
#     with open('mypic.jpg', 'rb') as image:
#         img = image.read()
#         #face_to_detect = bytearray(img) #library needs a image file and can't interpret bytearray 
#         face_to_detect = Image.open()
#         print("image reading done!")
#         #print(face_to_detect)
# except Exception as ex:
#     print("exception in reading image bytes {0}".format(ex.args))
#     has_exception = True


#post the image 
if has_exception != True:
    print("trying to post the image")
    #try:
    ##print(urllib.pathname2url('c:\mypic.jpg'))

    currentDir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    image = os.path.join(currentDir, "mypic.jpg")
    #image = urllib.pathname2url(image)
    print("image path is {0}".format(image))
    result = cf.face.detect(image,face_id=True,landmarks=False, attributes='age,gender,smile,emotion')
        #result = cf.face.detect(face_to_detect)
    print(result) 
   # except Exception as e:
    #    print("Error in detecting face: {0}".format(e.args))
    


    

