import nose
from nose.tools import *
from photosets import *

class testPhotoSets(object):

	def testFlickrPhotoSetGetInfo(self):
		v = FlickrPhotoSetGetInfo(photoset_id='72157627430799632')
		eq_(v.loaded,True)

	def testFlickrPhotoSetsGetList(self):
		v = FlickrPhotoSetsGetList()
		eq_(v.loaded,True)
		ok_(len(v.getSetIDs())>0,'No sets for the given API and User')
		
	def testFlickrPhotoSetsGetPhotos(self):
		v = FlickrPhotoSetsGetPhotos(photoset_id='72157627430799632')
		eq_(v.loaded,True)
		ok_(len(v.getPhotoIds())>0,'No sets for the given API and User')
        