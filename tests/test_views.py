import pytest
from django.core.urlresolvers import reverse
from django.http import Http404

from controlled_vocabularies import views
from .factories import VocabularyFactory, TermFactory, PropertyFactory


class TestAbout():

    def test_status_ok(self, rf):
        request = rf.get('/')
        response = views.about(request)
        assert response.status_code == 200

    def test_template_used(self, client):
        response = client.get(reverse('about'))
        assert response.templates[0].name == 'vocabularies/about.html'


class TestVocabularyList():

    @pytest.mark.django_db
    def test_status_ok(self, rf):
        request = rf.get('/')
        response = views.about(request)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_template_used(self, client):
        response = client.get(reverse('vocabulary_list'))
        assert response.templates[0].name == 'vocabularies/vocabulary_list.html'


class TestTermList():

    @pytest.mark.django_db
    def test_status_ok(self, rf):
        TermFactory(vocab_list=VocabularyFactory(name='Language'))
        request = rf.get('/')
        response = views.term_list(request, 'Language')
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_template_used(self, client):
        TermFactory(vocab_list=VocabularyFactory(name='Language'))
        response = client.get(reverse('term_list', args=['Language']))
        assert response.templates[0].name == 'vocabularies/term_list.html'



class TestAllVocabularies():

    @pytest.mark.django_db
    def test_status_ok(self, rf):
        request = rf.get('/')
        response = views.all_vocabularies(request)
        assert response.status_code == 200


class TestVerboseVocabularies():

    @pytest.mark.django_db
    def test_status_ok(self, rf):
        request = rf.get('/')
        response = views.verbose_vocabularies(request)
        assert response.status_code == 200


class TestVocabularyFile():

    @pytest.mark.django_db
    def test_status_ok(self, rf):
        VocabularyFactory(name='Language')
        request = rf.get('/')
        response = views.vocabulary_file(request, 'Language', 'XML')
        assert response.status_code == 200
