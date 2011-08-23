import nose
from nose.tools import *
from photos import *

class testPhotoSets(object):

	@classmethod
	def setup_class(self):
		self.photo_id = '5904161963'
        
	def testFlickrPhotosGetSizes(self):
		v = FlickrPhotosGetSizes(photo_id=self.photo_id)
		eq_(v.loaded,True)

	def testFlickrPhotosGetInfo(self):
		v = FlickrPhotosGetInfo(photo_id=self.photo_id)
		eq_(v.loaded,True)
		
	def testFlickrPhotosGetAllContexts(self):
		v = FlickrPhotosGetAllContexts(photo_id=self.photo_id)
		eq_(v.loaded,True)