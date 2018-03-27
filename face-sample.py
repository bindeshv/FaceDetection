import cognitive_face as cf
import urllib,os, json, time 


class Friend:
    def __init__(self, name, person_id, emotion, gender):
        self.name = name 
        self.person_id = person_id
        self.emotion = emotion
        self.gender = gender 

    def pretty_print(self):
        print("Detected friend %s gender is %s and emotions are %s" % (self.name,self.gender,self.emotion))



class IdentityAttribs:

    def __init__(self,gender,detected_emotions):
        self.gender = gender 
        self.emotions = detected_emotions #dict obj {} 


def parse_emotions(emotions):
    ret = '' 
  
    if (float(emotions['happiness']) * 100) > 45:
        ret += 'Happiness'

    if (float(emotions['anger']) * 100) > 45:
        ret += ' Anger'

    if (float(emotions['fear']) * 100) > 45:
        ret += ' Fear'

    if (float(emotions['neutral']) * 100) > 45:
        ret += ' Neutral'

    if  (float(emotions['sadness']) * 100) > 45:
            ret += ' Sadness'
    return ret 


def main():
    
    #load the key from json file 
    with open('keys.json') as data:
        keys = json.load(data)
        data.close()

    face_api_key = keys["api_key"]
    face_api_endpoint = keys["api_endpoint"]

    cf.Key.set(face_api_key)
    cf.BaseUrl.set(face_api_endpoint)
    friends = []

    #set image path 
    #detect current folder
    current_folder = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    images_folder = os.path.join(current_folder, "people")

    #create face group
    pg_id = "fg1"
    grp_resp = None
    grp_info = None 

    #check if this group already exists then delete it 
    #helpful while debugging, remove in prod 
    try:
        grp_info = cf.person_group.get(pg_id)
        if len(grp_info['personGroupId']) > 0:
            #delete the group 
            #print("found an existing person group named {}.skipping group creation".format(grp_info['personGroupId']))
            cf.person_group.delete(pg_id)

    except Exception as err:
        print("person group not found! {0}".format(err))


    
    grp_resp = cf.person_group.create(pg_id, "Default Group")

    
    #define Bindesh 
    p1 = cf.person.create(pg_id, "Bindesh")

    #store id 
    #ppl_id['bindesh'] = p1["personId"]
    image_path = os.path.join(images_folder, "bindesh")
    for file in os.listdir(image_path):
        url = os.path.join(image_path, file)
        print("Adding image {}".format(url))
        cf.person.add_face(url,pg_id,p1["personId"])

    #define 
    p2 = cf.person.create(pg_id, "ranvijay")



    image_path = os.path.join(images_folder, "ranvijay")
    for file in os.listdir(image_path):
        url = os.path.join(image_path, file)
        print("Adding image {}".format(url))
        cf.person.add_face(url,pg_id,p2["personId"])
    print("Image adding process completed!")
    print("Starting training..")
    cf.person_group.train(pg_id)

    #get the training status 
    training_status = cf.person_group.get_status(pg_id)
    while training_status['status'] != "succeeded":
        print("current training status is {0}".format(training_status['status']))
        time.sleep(10) #sleep for 25 sec 
        #recheck 
        training_status = cf.person_group.get_status(pg_id)

    print("training completed!") 
    print("\n waiting for input:")

    inp = 'x'
    while inp != 'X':
        print("please enter the name of the image to scan, X to exit\n")
        print("the image has to be either in the program folder or please provide full path")
        inp = input()
       
        if inp != 'X':
            print("processing image {0}".format(inp))
            #detect the faces in the uploaded image 
            #this will return the face ids of all the detected images 
            dtct_resp = cf.face.detect(inp, face_id=True, landmarks=False, attributes='age,gender,emotion')
            detected_faces = {} #stores IdentityAttribs objects 
            dtct_ids = []

            #extract all the face ids from the response json and store them inside an array
            #to be consumed by identify api call 
            for item in dtct_resp:
                detected_faces[item['faceId']] = IdentityAttribs(item['faceAttributes']['gender'], item['faceAttributes']['emotion'])
                dtct_ids.append(item['faceId'])


            #make a call identify the detected ids 
            idfy_rslts = cf.face.identify(dtct_ids, pg_id)

            for id_res in idfy_rslts:
                #get the person 
                person = cf.person.get(pg_id, id_res['candidates'][0]['personId'])
                dtct_fc = detected_faces.get(id_res['faceId'])
                f1 = Friend(person['name'],id_res['candidates'][0]['personId'], parse_emotions(dtct_fc.emotions),dtct_fc.gender )
                friends.append(f1)   

        #inp = 'X'
        for i,f in enumerate(friends):
            print("printing friend {0}".format(i))
            f.pretty_print()




main() 

    