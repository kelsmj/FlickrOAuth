import oauth2 as oauth
import time
import httplib2
import urlparse
import base64
import hmac

class APIKeys:
	"""Helper class to read the API Keys"""
	def __init__(self,filename):
		if filename is None:
			raise ValueError("No File Specified")
		self.filename = filename
		try:
		    fp = open("apikeys")
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
# Read the APIKeys
keys = APIKeys("apikeys")
		
# Set the API endpoint 
url = "http://www.flickr.com/services/oauth/request_token"
authorize_url = "http://www.flickr.com/services/oauth/authorize"
access_token_url = "http://www.flickr.com/services/oauth/access_token"

# Set the base oauth_* parameters along with any other parameters required
# for the API call.
params = {
    'oauth_timestamp': str(int(time.time())),
	'oauth_signature_method':"HMAC-SHA1",
    'oauth_version': "1.0",
	'oauth_callback': "http://www.mkelsey.com",
	'oauth_nonce': oauth.generate_nonce(),
	'oauth_consumer_key': keys.apikey
}

# Setup the Consumer with the api_keys given by the provider
consumer = oauth.Consumer(key=keys.apikey, secret=keys.apisecret)

# Create our request. Change method, etc. accordingly.
req = oauth.Request(method="GET", url=url, parameters=params)

# Create the signature
signature = oauth.SignatureMethod_HMAC_SHA1().sign(req,consumer,None)

# Add the Signature to the request
req['oauth_signature'] = signature

# Make the request to get the oauth_token and the oauth_token_secret
# I had to directly use the httplib2 here, instead of the oauth library.
h = httplib2.Http(".cache")
resp, content = h.request(req.to_url(), "GET")

#parse the content
request_token = dict(urlparse.parse_qsl(content))

print "Request Token:"
print "    - oauth_token        = %s" % request_token['oauth_token']
print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
print

# Create the token object with returned oauth_token and oauth_token_secret
token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])

# You need to authorize this app via your browser.
print "Go to the following link in your browser:"
print "%s?oauth_token=%s&perms=read" % (authorize_url, request_token['oauth_token'])
print

# Once you get the verified pin, input it
accepted = 'n'
while accepted.lower() == 'n':
    accepted = raw_input('Have you authorized me? (y/n) ')
oauth_verifier = raw_input('What is the PIN? ')

#set the oauth_verifier token
token.set_verifier(oauth_verifier)

# Now you need to exchange your Request Token for an Access Token
# Set the base oauth_* parameters along with any other parameters required
# for the API call.
access_token_parms = {
    'oauth_consumer_key': keys.apikey,
	'oauth_nonce': oauth.generate_nonce(),
	'oauth_signature_method':"HMAC-SHA1",
    'oauth_timestamp': str(int(time.time())),
	'oauth_token':request_token['oauth_token'],
	'oauth_verifier' : oauth_verifier
}

#setup request
req = oauth.Request(method="GET", url=access_token_url, parameters=access_token_parms)

#create the signature
signature = oauth.SignatureMethod_HMAC_SHA1().sign(req,consumer,token)

# assign the signature to the request
req['oauth_signature'] = signature

#make the request
h = httplib2.Http(".cache")
resp, content = h.request(req.to_url(), "GET")

#parse the response
access_token_resp = dict(urlparse.parse_qsl(content))

#write out a file with the oauth_token and oauth_token_secret
with open('token', 'w') as f:
	f.write(access_token_resp['oauth_token'] + '\n')
	f.write(access_token_resp['oauth_token_secret'])
f.closed

