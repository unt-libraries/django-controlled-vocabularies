from django.test import TestCase
from django.test import Client
from models import Vocabulary

class ResponseCodeTest(TestCase):

    def setUp(self):
        self.c = Client()
        Vocabulary(
            name='collections',
            label='collections',
            order='name',
            maintainer='joey',
            maintainerEmail='blah@tah.gaw',
            definition='collections',
        ).save()
        
    def tearDown(self):
        pass
        
    def test_main_page(self):
        response = self.c.get('/vocabularies/')
        self.assertEqual(response.status_code, 200)

    def test_all_verbose(self):
        response = self.c.get('/vocabularies/all-verbose/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.c.get('/vocabularies/about/')
        self.assertEqual(response.status_code, 200)

    def test_all(self):
        response = self.c.get('/vocabularies/all/')
        self.assertEqual(response.status_code, 200)

    def test_named_vocabulary(self):
        response = self.c.get('/vocabularies/collections/')
        self.assertEqual(response.status_code, 200)

    def test_named_vocabulary_output_methods(self):
        response = self.c.get('/vocabularies/collections/tkl/')
        self.assertEqual(response.status_code, 200)
        response = self.c.get('/vocabularies/collections/py/')
        self.assertEqual(response.status_code, 200)
        response = self.c.get('/vocabularies/collections/json/')
        self.assertEqual(response.status_code, 200)
        response = self.c.get('/vocabularies/collections/xml/')
        self.assertEqual(response.status_code, 200)
