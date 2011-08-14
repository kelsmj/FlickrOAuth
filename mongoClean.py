import pymongo
import gridfs

mongo = pymongo.Connection("localhost", 27017)
db = mongo['flickr']
photosets = db['photosets']
photosets.remove()
fs = gridfs.GridFS(db)
for o in db.fs.files.find({}):
    fs.delete(o["_id"])