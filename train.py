import cognitive_face as cf 
import urllib,json,os,time 

class TrainingModel:

    def __init__(self):
        #init images folder 
        current_dir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
        self.img_dir = os.path.join(current_dir, "people")

        #init cf sdk 
        self.api_endpoint = "https://southcentralus.api.cognitive.microsoft.com/face/v1.0/"
        cf.Key.set("")
        cf.BaseUrl.set(self.api_endpoint)

        #group id 
        self.grp_id = "bindeshsfriends"


    def create_face_group(self):
        
        try:

            grp_id = cf.person_group.get(self.grp_id)
        
        #if the group already exists then delete for now
            print("grp{0}".format(grp_id))
            cf.person_group.delete(self.grp_id)
        except Exception as e:
            print(e.args)


       
            
        cf.person_group.create(self.grp_id, "Friends")
        p1 = cf.person.create(self.grp_id, "Bindesh")
        image_path = os.path.join(self.img_dir, "bindesh")
        print("image path:{0}".format(image_path))
        for file in os.listdir(image_path):
            url = os.path.join(image_path, file)
            print("adding {0}".format(url))
            cf.person.add_face(url,self.grp_id,p1)

        p2 = cf.person.create(self.grp_id, "ranvijay")
        image_path = os.path.join(self.img_dir, "ranvijay")
        print("image path:{0}".format(image_path))
        for file in os.listdir(image_path):
            url = os.path.join(image_path, file)
            print("adding {0}".format(url))
            cf.person.add_face(url,self.grp_id,p2)

        


    def train_model(self):
        cf.person_group.train(self.grp_id)
        print("Training started...")
        status = cf.person_group.get_status(self.grp_id) 
        print(status)
        if status['status'] != 'failed':
            while status['status'] != "suceeded":
                print("Status:{0}".format(status[0]))
                time.sleep(25) #sleep for 25 sec 
                #recheck 
                status = json.parse(cf.person_group.get_status()) 
        else:
            print("training failed!") 


    def detect_images(self):
        resp = cf.face.detect("sample-image.jpg")
        print("resp:")
        print(resp)         




tm = TrainingModel()
tm.create_face_group()
tm.train_model()
tm.detect_images()


