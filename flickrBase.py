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
			'oauth_consumer_key':self.consumer.key
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
		