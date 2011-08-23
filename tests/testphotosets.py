import nose
from nose.tools import *
from photosets import *

class testPhotoSets(object):

	@classmethod
	def setup_class(self):
		self.photoset_id = '72157626996532431'
		self.photo_id = '5904161963'
        
	def testFlickrPhotoSetGetInfo(self):
		v = FlickrPhotoSetGetInfo(photoset_id=self.photoset_id)
		eq_(v.loaded,True)

	def testFlickrPhotoSetsGetList(self):
		v = FlickrPhotoSetsGetList()
		eq_(v.loaded,True)
		ok_(len(v.getSetIDs())>0,'No sets for the given API and User')
		
	def testFlickrPhotoSetsGetPhotos(self):
		v = FlickrPhotoSetsGetPhotos(photoset_id=self.photoset_id)
		eq_(v.loaded,True)
		ok_(len(v.getPhotoIds())>0,'No sets for the given API and User')

        