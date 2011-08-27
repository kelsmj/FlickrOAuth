from flickrBase import *

#Returns all visible sets and pools the photo belongs to.		
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
			
			
#Fetch a list of recent photos from the calling users' contacts.
class FlickrPhotosGetContactsPhotos(FlickrApiMethod):
	name = 'flickr.photos.getContactsPhotos'
	
	def __init__(self,nojsoncallback=True,format='json',parameters=None):
		FlickrApiMethod.__init__(self,nojsoncallback,format,parameters)
	
	def getParameters(self):
		p={
			#For some reason this api call expects
			#oauth_signature_method as a parameter
			'oauth_signature_method': "HMAC-SHA1",
			'method':self.name
		}
		
		return p

#Fetch a list of recent public photos from a users' contacts.
class FlickrPhotosGetContactsPublicPhotos(FlickrApiMethod):
	name = 'flickr.photos.getContactsPublicPhotos'
	
	def __init__(self,nojsoncallback=True,format='json',parameters=None,user_id=None):
		self.user_id=user_id
		FlickrApiMethod.__init__(self,nojsoncallback,format,parameters)
		
	def getParameters(self):
		p={
			'method':self.name,
			'user_id':self.user_id
		}
		return p
		
#Returns next and previous photos for a photo in a photostream.
class FlickrPhotosGetContext(FlickrApiMethod):
	name = 'flickr.photos.getContext'
	
	def __init__(self,nojsoncallback=True,format='json',parameters=None,photo_id=None):
		self.photo_id=photo_id
		FlickrApiMethod.__init__(self,nojsoncallback,format,parameters)
		
	def getParameters(self):
		p={
			'method':self.name,
			'photo_id':self.photo_id
		}
		return p

#Gets a list of photo counts for the given date ranges for the calling user.
class FlickrPhotosGetCounts(FlickrApiMethod):
	name = 'flickr.photos.getCounts'
	
	def __init__(self,nojsoncallback=True,format='json',parameters=None):
		FlickrApiMethod.__init__(self,nojsoncallback,format,parameters)
		
	def getParameters(self):
		p={
			'method':self.name
		}
		return p

		
#Returns the available sizes for a photo. The calling user must have permission to view the photo.
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
			
#Get information about a photo. The calling user must have permission to view the photo.
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
