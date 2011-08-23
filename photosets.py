from flickrBase import *

class FlickrPhotoSetGetInfo(FlickrApiMethod):
	name='flickr.photosets.getInfo'
	def __init__(self,nojsoncallback=True,format='json',parameters=None,photoset_id=None):
		self.photoset_id = photoset_id
		FlickrApiMethod.__init__(self,nojsoncallback,format,parameters)
	
	def getParameters(self):
		p={
			'method':'flickr.photosets.getInfo',
			'photoset_id':self.photoset_id
		}
		return p
	
class FlickrPhotoSetsGetList(FlickrApiMethod):
	name='flickr.photosets.getList'
	def __init__(self,nojsoncallback=True,format='json',parameters=None,user_id=None):
		FlickrApiMethod.__init__(self,nojsoncallback,format,parameters)
		
	def getParameters(self):
		p={
			'method':'flickr.photosets.getList'
		}
		
		return p
	
	def getSetIDs(self):
		l=[]
		for o in self.json["photosets"]["photoset"]:
			l.append(o["id"])
		return l

class FlickrPhotoSetsGetPhotos(FlickrApiMethod):
	name='flickr.photosets.getPhotos'
	def __init__(self,nojsoncallback=True,format='json',parameters=None,photoset_id=None,page=1):
		self.photoset_id = photoset_id
		self.page = page
		FlickrApiMethod.__init__(self,nojsoncallback,format,parameters)
		
		
	def getParameters(self):
		p={
			'method':'flickr.photosets.getPhotos',
			'media':'photos',
			'per_page':500,
            'page':self.page,
            'photoset_id':self.photoset_id
		}
		return p
		
	def getPhotoIds(self):
		l =[]
		if(self.loaded):
			for o in self.json["photoset"]["photo"]:
				l.append(o["id"])
			while(self.page < self.json["photoset"]["pages"]):
				self.page = self.page + 1
				if(self.makeCall()):
					for o in self.json["photoset"]["photo"]:
						l.append(o["id"])
		return l
		
		