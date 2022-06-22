from django.test import TestCase

from .lbs import clean_string

class CleanStringTestCase(TestCase):

	dirty_s = '~`а!@#н$%^д&*(р)-_+=/*-+/?.>,<\"е\';:[{] }.й!|\\'
	clean_s = ''

	def setUp(self):
		self.clean_s = clean_string(self.dirty_s)

	def test_string(self):
		self.assertEqual(self.clean_s, 'a-n-d-r-e-j') 