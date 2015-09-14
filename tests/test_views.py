import pytest
from django.core.urlresolvers import reverse
from django.http import Http404

from controlled_vocabularies import views
from .factories import VocabularyFactory, TermFactory

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

    def test_context_var(self, client):
        VocabularyFactory.create_batch(10)
        response = client.get(reverse('vocabulary_list'))
        assert response.context['vocabularies'].count() == 10


class TestTermList():

    def test_status_ok_with_matching_vocabulary(self, rf):
        TermFactory(vocab_list=VocabularyFactory(name='Language'))
        request = rf.get('/')
        response = views.term_list(request, 'Language')
        assert response.status_code == 200

    def test_raises_http404_without_matching_vocabulary(self, rf):
        TermFactory(vocab_list=VocabularyFactory(name='Language'))
        request = rf.get('/')
        with pytest.raises(Http404):
            views.term_list(request, 'Nothing')

    def test_template_used(self, client):
        TermFactory(vocab_list=VocabularyFactory(name='Language'))
        response = client.get(reverse('term_list', args=['Language']))
        assert response.templates[0].name == 'vocabularies/term_list.html'

    def test_context_vars(self, client):
        # Make 4 terms that should be retrieved.
        vocab = VocabularyFactory(name='Language')
        terms = TermFactory.create_batch(4, vocab_list=vocab)
        # And make 4 that shouldn't.
        TermFactory.create_batch(4)

        response = client.get(reverse('term_list', args=['Language']))
        assert response.context['vocabulary'] == vocab
        for term in response.context['terms']:
            assert term['term_item'] in terms
        assert response.context['domain'] == 'http://purl.org/NET/UNTL/'


class TestAllVocabularies():

    def test_status_ok(self, rf):
        request = rf.get('/')
        response = views.all_vocabularies(request)
        assert response.status_code == 200

    def test_vocab_dict(self, rf):
        terms = TermFactory.create_batch(4)
        request = rf.get('/')
        response = views.all_vocabularies(request)
        for term in terms:
            assert term.vocab_list.name in response.content
            assert term.name in response.content


class TestVerboseVocabularies():

    def test_status_ok(self, rf):
        request = rf.get('/')
        response = views.verbose_vocabularies(request)
        assert response.status_code == 200

    # Passes inconsistently due to attempting to sort by order field in wrong model.
    @pytest.mark.xfail
    def test_ordered_term_objects_with_order_attributes(self, rf):
        # Create terms with a specified order.
        vocab = VocabularyFactory(name='Language')
        TermFactory(order=3, vocab_list=vocab)
        TermFactory(order=1, vocab_list=vocab)
        TermFactory(order=2, vocab_list=vocab)

        request = rf.get('/')
        response = views.verbose_vocabularies(request)

        # Make sure the order is followed by asserting the terms appear in the specified order.
        assert (response.content.find("'order': 1") <
                response.content.find("'order': 2") <
                response.content.find("'order': 3"))

    def test_vocab_dict(self, rf):
        terms = TermFactory.create_batch(4)
        request = rf.get('/')
        response = views.verbose_vocabularies(request)
        for term in terms:
            assert term.vocab_list.name in response.content
            assert term.name in response.content
            assert term.label in response.content
            if term.order is not None:
                assert "'order': {}".format(term.order) in response.content
            assert 'http://purl.org/NET/UNTL/vocabularies/{}/#{}'.format(
                term.vocab_list.name, term.name)


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
