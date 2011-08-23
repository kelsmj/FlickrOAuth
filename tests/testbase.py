import nose
from nose.tools import *
from photosets import *

class testBase(object):

	def testAPIKeys(self):
		a = APIKeys()
		ok_(len(a.apikey)>0,'No API Key')
		ok_(len(a.apisecret)>0,'No API Secret')

	def testTokenKeys(self):
		t = TokenKeys()
		ok_(len(t.token)>0,'No Token Key')
		ok_(len(t.secret)>0,'No Secret')