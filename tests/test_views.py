import pytest
from django.core.urlresolvers import reverse
from django.http import Http404

from controlled_vocabularies import views
from .factories import VocabularyFactory, TermFactory, PropertyFactory

pytestmark = pytest.mark.django_db


class TestAbout():

    def test_status_ok(self, rf):
        request = rf.get('/')
        response = views.about(request)
        assert response.status_code == 200

    def test_template_used(self, client):
        response = client.get(reverse('about'))
        assert response.templates[0].name == 'vocabularies/about.html'


class TestVocabularyList():

    def test_status_ok(self, rf):
        request = rf.get('/')
        response = views.about(request)
        assert response.status_code == 200

    def test_template_used(self, client):
        response = client.get(reverse('vocabulary_list'))
        assert response.templates[0].name == 'vocabularies/vocabulary_list.html'

    def test_context_var(self, rf):
        pass


class TestTermList():

    def test_status_ok_with_matching_vocabulary(self, rf):
        TermFactory(vocab_list=VocabularyFactory(name='Language'))
        request = rf.get('/')
        response = views.term_list(request, 'Language')
        assert response.status_code == 200

    def test_status_404_without_matching_vocabulary(self, rf):
        pass

    def test_template_used(self, client):
        TermFactory(vocab_list=VocabularyFactory(name='Language'))
        response = client.get(reverse('term_list', args=['Language']))
        assert response.templates[0].name == 'vocabularies/term_list.html'

    def test_context_vars(self, rf):
        pass


class TestAllVocabularies():

    def test_status_ok(self, rf):
        request = rf.get('/')
        response = views.all_vocabularies(request)
        assert response.status_code == 200

    def test_vocab_dict(self, rf):
        pass


class TestVerboseVocabularies():

    def test_status_ok(self, rf):
        request = rf.get('/')
        response = views.verbose_vocabularies(request)
        assert response.status_code == 200

    def test_ordered_term_objects_with_order_attributes(self, rf):
        pass

    def test_ordered_term_objects_without_order_attributes(self, rf):
        pass

    def test_vocab_dict(self, rf):
        pass


class TestVocabularyFile():

    def test_status_ok_type_xml(self, rf):
        VocabularyFactory(name='Language')
        request = rf.get('/')
        response = views.vocabulary_file(request, 'Language', 'XML')
        assert response.status_code == 200

    def test_status_ok_type_py(self, rf):
        VocabularyFactory(name='Language')
        request = rf.get('/')
        response = views.vocabulary_file(request, 'Language', 'PY')
        assert response.status_code == 200

    def test_status_ok_type_json(self, rf):
        VocabularyFactory(name='Language')
        request = rf.get('/')
        response = views.vocabulary_file(request, 'Language', 'JSON')
        assert response.status_code == 200

    def test_status_ok_type_tkl(self, rf):
        VocabularyFactory(name='Language')
        request = rf.get('/')
        response = views.vocabulary_file(request, 'Language', 'TKL')
        assert response.status_code == 200
