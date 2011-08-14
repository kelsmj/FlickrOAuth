import pymongo
import gridfs
from flickrDownload import *

mongo = pymongo.Connection("localhost", 27017)
db = mongo['flickr']
photosets = db['photosets']
fs = gridfs.GridFS(db)

def GetPhotoInfo(SetID):
    photoinfo=[]
    for photoid in FlickrPhotoSetsGetPhotos(photoset_id=id).getPhotoIds():
        sizes=[]
        jsonPhoto = FlickrPhotosGetInfo(photo_id=photoid).json
        jsonPhoto["photosizes"] = FlickrPhotosGetSizes(photo_id=photoid).json
        photoinfo.append(jsonPhoto)
    return photoinfo
    
def ReadPhotoFromFlickr(source):
    opener = urllib2.build_opener()
    page = opener.open(source)
    photo = page.read()
    return photo
    
def WritePhotoToGridFS(size,photoid,source):
    s = size.replace(' ','_')
    fs.put(ReadPhotoFromFlickr(source),size=s,id=photoid)

def WritePhotoFromMongoToDisk(objectid,dir):
    f = db.fs.files.find_one({"_id":objectid})
    if(f != None):
        out = fs.get(objectid)
        out.read()
        if not os.path.exists(dir):
            os.makedirs(dir)
        fout = open(os.path.join(dir,f['id']+'.jpg'),"wb")
        fout.write(out.read())
        fout.close()
        return True
    else:
        return False
    

#Get the List of PhotoSet IDs
setList = FlickrPhotoSetsGetList().getSetIDs()

print photosets.count()
#Loop through list of SetIDs and get PhotoSet Info
for id in setList:
    ps = photosets.find_one({"photoset.id":id})
    if(ps == None):
        setinfo = FlickrPhotoSetGetInfo(photoset_id=id)
        setinfo.json["photoinfo"] = GetPhotoInfo(id)
        photosets.insert(setinfo.json)
    else:
        print 'Set already in collection'
photos = []
start = time.time()
counter = 0
#Loop through the photosets in mongo
for photoset in photosets.find({}):
    setTitle = photoset["photoset"]["title"]["_content"]
    for photoinfo in photoset["photoinfo"]:
        photoid = photoinfo["photo"]["id"]
        if photoid in photos:
            print 'Photo ' + photoid + ' already in list'
        else:
            for s in photoinfo["photosizes"]["sizes"]["size"]:
                #Find file where id = photoid and size = label
                file = db.fs.files.find_one({"id":photoid,"size":s["label"].replace(' ','_')})
                if(file == None):
                    print 'Writing photo ' + photoid + ' (' + s["label"] + ') to GridFS'
                    WritePhotoToGridFS(size=s["label"],photoid=photoid,source=s["source"])
                else:
                    print 'PhotoID ' + photoid + ' already exists in collection'
            counter = counter + 1
            print counter
            photos.append(photoid)

elapsed = (time.time() - start)
print 'It took ' + str(elapsed) + ' to download ' + str(len(photos)) + ' of each size and store in GridFS'
    

