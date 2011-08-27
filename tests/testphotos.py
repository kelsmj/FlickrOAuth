import nose
import time
from nose.tools import *
from photos import *


class testPhotoSets(object):

	@classmethod
	def setup_class(self):
		self.photo_id = '5904161963'
		self.contact_user_id = '47585052@N00'
        
	def testFlickrPhotosGetSizes(self):
		v = FlickrPhotosGetSizes(photo_id=self.photo_id)
		eq_(v.loaded,True)

	def testFlickrPhotosGetInfo(self):
		v = FlickrPhotosGetInfo(photo_id=self.photo_id)
		eq_(v.loaded,True)
		
	def testFlickrPhotosGetAllContexts(self):
		v = FlickrPhotosGetAllContexts(photo_id=self.photo_id)
		eq_(len(v.json["set"]),2)#photo belongs to 2 sets
		eq_(v.loaded,True)
		
	def testFlickrPhotosGetContactsPhotos(self):
		v = FlickrPhotosGetContactsPhotos()
		eq_(len(v.json["photos"]["photo"]),5)#my contact has 5 photos
		eq_(v.loaded,True)
		z = FlickrPhotosGetContactsPhotos(parameters={'count':2})
		eq_(len(z.json["photos"]["photo"]),2)#limit to 2
		
	def testFlickrPhotosGetContactsPublicPhotos(self):
		v = FlickrPhotosGetContactsPublicPhotos(user_id = self.contact_user_id)
		eq_(v.loaded,True)
		eq_(len(v.json["photos"]["photo"]),5)
		
	def testFlickrPhotosGetContext(self):
		v = FlickrPhotosGetContext(photo_id = self.photo_id)
		eq_(v.loaded,True)		
		
	def testFlickrPhotosGetCounts(self):
		v = FlickrPhotosGetCounts(parameters={'dates':int(time.time()-30000)})
		eq_(v.loaded,True)			