import oauth2 as oauth
import time
import httplib2
import urlparse
import json
import urllib2
import os
import base64
import unicodedata


class APIKeys(object):
	"""Base class to read the APIKeys from file"""
	
	def __init__(self,filename='apikeys'):
		try:
		    fp = open(filename)
		except IOError as e:
		    if e.errno == errno.EACCESS:
		        print "file does not exists"
		    # Not a permission error.
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
			if e.errno == errno.EACCESS:
				print "file does not exists"
			# Not a permission error.
			raise
		else:
			with fp:
				self.token = fp.readline().rstrip('\n')
				self.secret = fp.readline()
				fp.close()

class FlickrPhotoSet(object):
	"""Base class that represents a photoSet"""
	
	def __init__(self,set_id):
		self.photo_set_id = set_id
		self.photos = []
		
class FlickrPhoto(object):
	"""Base class that represents a flickr photo"""
	
	def __init__(self,photo_id):
		self.photo_id = photo_id
		self.photoInfo = FlickrPhotosGetInfo(photo_id =self.photo_id)
		self.tags = self.getTags()
		self.photoSets = []
		self.title = self.photoInfo.json["photo"]["title"]["_content"]
		self.description = ""
		self.fileNames = self.getFileNames();
		self.fileDir = './pictures/'
    
	def getFileNames(self):
		photoSizes = FlickrPhotosGetSizes(photo_id = self.photo_id)
		files = {}
		if(photoSizes.loaded):
			for o in photoSizes.json["sizes"]["size"]:
				files[o["label"].replace(' ', '_')] =self.title.replace(' ', '_') + '_' + self.photo_id + o["source"][-4:]
		return files
	
	def getTags(self):
		t = []
		for o in self.photoInfo.json["photo"]["tags"]["tag"]:
			t.append(o["_content"])
			
		return t
	
		
	
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
			'method':'flickr.photosets.getList',
			'media':'photos',
			'per_page':500,
            'page':self.page,
            'photoset_id':self.photoset_id
		}
		
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
			dir = './pictures/' + o["label"].replace(' ', '_')
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


set = FlickrPhotoSetsGetList()

'''
print "Please enter a photo id:",
photoId = raw_input()
print "Fetching Photo"


photoSizes = FlickrPhotosGetSizes(photo_id = photoId)
if(photoSizes.makeCall()):
	print "API Call Success! Writing Photos to Disk"
	photoSizes.writePhotos()
else:
	print "API Call Failed"
'''

'''
photos = FlickrPeopleGetPhotos(user_id = 'me')

with open('photoIds.txt', 'w') as f:
	for o in photos.getPhotoIds():
		f.write(o + '\n')
f.closed



sets = FlickrPhotoSetsGetList()

with open('setIds.txt', 'w') as f:
	for o in sets.getSetIDs():
		f.write(o + '\n')
f.closed
'''
photoSets = []
fpSets = open('setIds.txt')
photoSets = fpSets.readlines()
fpSets.close()

photos =[]
fp = open('photoIds.txt')
photos = fp.readlines()
fp.close()


photo = FlickrPhoto(photo_id =photos[1].rstrip('\n'))
print photo.fileNames
print photo.title
print photo.tags
'''
f = FlickrPhotosGetSizes(photo_id =l[1].rstrip('\n'))
if(f.makeCall()):
	f.writePhotos()
else:
	print 'API Failed'
'''