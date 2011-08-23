from flickrBase import *

class FlickrPhotosGetAllContexts(FlickrApiMethod):
	name = 'flickr.photos.getAllContexts'
	
	def __init__(self,nojsoncallback=True,format='json',parameters=None,photo_id=None):
		self.photo_id=photo_id
		FlickrApiMethod.__init__(self,nojsoncallback,format,parameters)
		
	def getParameters(self):
		p={
			'method':self.name,
			'photo_id':self.photo_id
		}
		return p
			
class FlickrPhotosGetSizes(FlickrApiMethod):
	name ='flickr.photos.getSizes'

	def __init__(self,nojsoncallback=True,format='json',parameters=None,photo_id=None):
		self.photo_id = photo_id
		FlickrApiMethod.__init__(self,nojsoncallback,format,parameters)
		

	def getParameters(self):
		p ={
			'method':self.name,
			'photo_id':self.photo_id
		}
		return p
	
	def writePhotos(self):
		for o in self.json["sizes"]["size"]:
			opener = urllib2.build_opener()
			page = opener.open(o["source"])
			my_picture = page.read()
			dir = './pictures/' + o["label"]
			if not os.path.exists(dir):
				os.makedirs(dir)
			filename = self.photo_id + o["source"][-4:]
			print filename
			fout = open(os.path.join(dir,filename),"wb")
			fout.write(my_picture)
			fout.close()
			

class FlickrPhotosGetInfo(FlickrApiMethod):
	name = 'flickr.photos.getInfo'

	def __init__(self,nojsoncallback=True,format='json',parameters=None,photo_id=None):
		self.photo_id = photo_id
		FlickrApiMethod.__init__(self,nojsoncallback,format,parameters)
		
		
	def getParameters(self):
		p={
			'method':self.name,
			'photo_id':self.photo_id
			}
		return p
