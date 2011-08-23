import oauth2 as oauth
import time
import httplib2
import urlparse
import json
import urllib2
import os
import base64
import unicodedata
import pickle
import pprint

class APIKeys(object):
	"""Base class to read the APIKeys from file"""
	
	def __init__(self,filename='apikeys'):
		try:
		    fp = open(filename)
		except IOError as e:
		    raise
		else:
		    with fp:
				self.apikey = fp.readline().rstrip('\n')
				self.apisecret = fp.readline()
				fp.close()
				
class TokenKeys(object):
	"""Base class to read the Access Tokens"""
	
	def __init__(self,filename='token'):
		try:
			fp = open(filename)
		except IOError as e:
			raise
		else:
			with fp:
				self.token = fp.readline().rstrip('\n')
				self.secret = fp.readline()
				fp.close()

class FlickrApiMethod(object):
	"""Base class for Flickr API calls"""
	
	def __init__(self,nojsoncallback=True,format='json',parameters=None):
		apifile = APIKeys()
		tokenfile = TokenKeys()
		
		self.loaded = False
		self.consumer = oauth.Consumer(key=apifile.apikey, secret=apifile.apisecret)
		self.token = oauth.Token(tokenfile.token, tokenfile.secret)
		
		if nojsoncallback:
			self.nojsoncallback = 1
		else:
			self.nojsoncallback = 0
		if not parameters:
			parameters = {}
			
		self.url = "http://api.flickr.com/services/rest"
		
		defaults = {
			'format':format,
			'nojsoncallback':self.nojsoncallback,
			'signature_method': "HMAC-SHA1",
			'oauth_token':self.token.key,
			'oauth_consumer_key':self.consumer.key,
		}
		
		defaults.update(parameters)
		self.parameters = defaults
		if self.makeCall():
			self.loaded = True
			
	def makeCall(self):
		uniques = {
			'oauth_timestamp': str(int(time.time())),
			'oauth_nonce': oauth.generate_nonce(),
		}
		self.parameters.update(uniques)
		self.parameters.update(self.getParameters())
		req = oauth.Request(method="GET", url=self.url, parameters=self.parameters)
		req['oauth_signature'] = oauth.SignatureMethod_HMAC_SHA1().sign(req,self.consumer,self.token)
		h = httplib2.Http(".cache")
		
		resp, content = h.request(req.to_url(), "GET")
		self.content = content
		self.json = json.loads(content)
		
		if self.json["stat"] == "ok":
			return True
		else:
			return False
	
	def getParameters(self):
		raise NotImplementedError

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
		
class FlickrPeopleGetPhotos(FlickrApiMethod):
    name = 'flickr.people.getPhotos'

    def __init__(self,nojsoncallback=True,format='json',parameters=None,user_id=None,page=1):
        self.user_id = user_id
        self.page = page
        FlickrApiMethod.__init__(self,nojsoncallback,format,parameters)
        

    def getParameters(self):
        p={
            'method':'flickr.people.getPhotos',
            'oauth_signature_method': "HMAC-SHA1",
            'user_id':self.user_id,
            'per_page':500,
            'page':self.page
        }
        return p
    
    def getPhotoIds(self):
    	l = []
    	if(self.makeCall()):
    		p = self.json["photos"]["page"]
    		for o in self.json["photos"]["photo"]:
    			l.append(o["id"])
    		while(self.page < self.json["photos"]["pages"]):
    			self.page = self.page + 1
    			if(self.makeCall()):
    				for o in self.json["photos"]["photo"]:
    					l.append(o["id"])
    	return l
				

class FlickrPhotosGetSizes(FlickrApiMethod):
	name ='flickr.photos.getSizes'

	def __init__(self,nojsoncallback=True,format='json',parameters=None,photo_id=None):
		self.photo_id = photo_id
		FlickrApiMethod.__init__(self,nojsoncallback,format,parameters)
		

	def getParameters(self):
		p ={
			'method':'flickr.photos.getSizes',
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
			'method':'flickr.photos.getInfo',
			'photo_id':self.photo_id
			}
		return p


class FlickrPhotoSet(object):
	"""Base class that represents a photoSet"""
	
	def __init__(self,photoset_id):
		self.photoset_id = photoset_id
		self.photoSet = FlickrPhotoSetGetInfo(photoset_id = self.photoset_id)
		self.title = self.photoSet.json["photoset"]["title"]["_content"]
		self.photos = {}
		self.photoIds = FlickrPhotoSetsGetPhotos(photoset_id=self.photoset_id).getPhotoIds()
		self.count = len(self.photoIds)
		self.fileDir = './pictures/' + self.title + '/'
		
		print 'Fetching ' + str(len(self.photoIds)) + ' in the set ' + self.title
		for o in self.photoIds:
			photo = FlickrPhoto(photo_id = o)
			#print 'Fetched ' + photo.photo_id + ':' + photo.title
			self.photos[o] = photo
			
	def writePhotos(self):
		for o in self.photos:
			for s in self.photos[o].sources:
				opener = urllib2.build_opener()
				page = opener.open(self.photos[o].sources[s])
				my_picture = page.read()
				dir = self.fileDir + s
				if not os.path.exists(dir):
					os.makedirs(dir)
				filename = self.photos[o].photo_id + self.photos[o].sources[s][-4:]
				print 'Writing ' + os.path.join(dir,filename)
				fout = open(os.path.join(dir,filename),"wb")
				fout.write(my_picture)
				fout.close()
			
class FlickrPhoto(object):
	"""Base class that represents a flickr photo"""
	
	def __init__(self,photo_id):
		self.photo_id = photo_id
		self.photoInfo = FlickrPhotosGetInfo(photo_id =self.photo_id)
		self.tags = self.getTags()
		self.photoSizes = FlickrPhotosGetSizes(photo_id = self.photo_id)
		self.photoSets = []
		self.title = self.photoInfo.json["photo"]["title"]["_content"]
		self.description = ""
		self.fileNames = self.getFileNames(photoSizes=self.photoSizes);
		self.sources = self.getSources(photoSizes=self.photoSizes);
		
    
	def getFileNames(self,photoSizes):
		files = {}
		if(photoSizes.loaded):
			for o in photoSizes.json["sizes"]["size"]:
				files[o["label"]] =self.title.replace(' ', '_') + '_' + self.photo_id + o["source"][-4:]
		return files
	
	def getSources(self,photoSizes):
		sources = {}
		if(photoSizes.loaded):
			for o in photoSizes.json["sizes"]["size"]:
				sources[o["label"].replace(' ', '_')] = o["source"]
		return sources
		
	def getTags(self):
		t = []
		for o in self.photoInfo.json["photo"]["tags"]["tag"]:
			t.append(o["_content"])
		return t
	
