from firebase import Firebase

config = {

    "apiKey": "AIzaSyBOx62bYTkuIGgV3TT0p93AgJUebXFsfEA",
  "authDomain": "sih-2020-fighters.firebaseapp.com",
  "databaseURL": "https://sih-2020-fighters.firebaseio.com",
  "projectId": "sih-2020-fighters",
  "storageBucket": "sih-2020-fighters.appspot.com",
  "messagingSenderId": "1047673300805",
  "appId": "1:1047673300805:web:f33fe441306cc08b90c02c",
  "measurementId": "G-KVJTKBCKCC"

}

firebase = Firebase(config)

db = firebase.database()
storage = firebase.storage()

def get_image_attribs(col,type,company):
    ref=db.child('assets')
    for img in ref.get().each():
        key = img.key()
        res = img.val()
        
        
        l = []
        if res['attribs']==company+'_'+col+'_'+type:
            for i in res['view']:
                l.append(res['view'][i])
        return l



def insertImageStorage(id,path):
    ref = storage.child("images/ID"+str(id)+"/inputs/0")
    ref.put(path)
    url =storage.child("images/ID"+str(id)+"/inputs/0").get_url(1)
    print(url)
    return str(url)


def updateImageStorage(main_id,res_id,path):
    ref = storage.child("images/ID"+str(main_id)+"/inputs/"+str(res_id))
    ref.put(path)
    url =storage.child("images/ID"+str(main_id)+"/inputs/"+str(res_id)).get_url(1)
    print(url)
    return str(url)


def insertURLDB(path):
    ref = db.child('images')
    x = ref.get()
   
    if x.val()!=None:
        count = len(list(x.val()))
    else:
        count=0
   
  
    count = count
    for i in range(len(path)):
        ref_path = "images/ID"+str(count)+"/inputs/"+str(i)
        data = {
        "id":"ID"+str(i),
        "url":path
        }
        db.child(ref_path).set(data)
    return count



def insertImageDB(path):
    ref = db.child('images')
    x = ref.get()
    print(x.val())
    if x.val()!=None:
        count = len(list(x.val()))
    else:
        count=0
    url = insertImageStorage(count,path)
    data = {
        "id":"ID"+str(count),
        "url":url
    }
    ref_path = "images/ID"+str(count)+"/inputs/0"
    db.child(ref_path).set(data)
    return count



def updateImageDB(id,path):
    ref = db.child('images/ID'+str(id)+'/inputs')
    x = ref.get()
    if x.val()!=None:
        count = len(list(x.val()))
   
        url = updateImageStorage(id,count,path)
        data = {
            "id":"ID"+str(count),
            "url":url
        }
        db.child('images/ID'+str(id)+'/inputs/'+str(count)).set(data)
        return data["url"]
    else:
        return ''


def getImageFromDB(id):
    ref = db.child('images/ID'+str(id)+'/inputs/').get()
    data = ref.val()
  
    l_urls=[]
    for i in data:
        l_urls.append(i['url'])
    return l_urls




def outputsToStorage(main_id,res_id,path):
    ref = storage.child("images/ID"+str(main_id)+"/outputs/"+str(res_id))
    ref.put(path)
    url =storage.child("images/ID"+str(main_id)+"/outputs/"+str(res_id)).get_url(1)
    print(url)
    return str(url)

def outputsToDB(id,path):
    ref = db.child('images/ID'+str(id)+'/outputs')
    x = ref.get()
    if x.val()!=None:
        count = len(list(x.val()))
    else:
        count=0
    url = outputsToStorage(id,count,path)
    data = {
        "id":"ID"+str(count),
        "url":url
    }
    db.child('images/ID'+str(id)+'/outputs/'+str(count)).set(data)
    return data["url"]
    





