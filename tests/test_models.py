import pytest
from django.contrib.sites.models import Site

from controlled_vocabularies.models import Vocabulary, Term, Property
from . import factories

pytestmark = pytest.mark.django_db

LINK = "<a href='http://{}/admin/vocabularies/{}/{}'>{}</a>"


class TestVocabulary:
    def test_save(self):
        vocab = factories.VocabularyFactory.build()
        assert Vocabulary.objects.all().count() == 0
        vocab.save()
        assert Vocabulary.objects.all().count() == 1

    def test_save_strips_whitespace(self):
        vocab = factories.VocabularyFactory(name=' spaces ', label=' spaces ')
        assert vocab.name == 'spaces'
        assert vocab.label == 'spaces'

    def test_str(self):
        vocab = factories.VocabularyFactory()
        assert str(vocab) == vocab.name


class TestTerm:
    def test_str(self):
        term = factories.TermFactory()
        assert str(term) == term.name

    def test_save(self):
        term = factories.TermFactory.build(vocab_list=factories.VocabularyFactory())
        assert Term.objects.all().count() == 0
        term.save()
        assert Term.objects.all().count() == 1

    def test_save_strips_whitespace(self):
        vocab = factories.TermFactory(name=' spaces ', label=' spaces ')
        assert vocab.name == 'spaces'
        assert vocab.label == 'spaces'

    def test_get_vocab(self):
        term = factories.TermFactory()
        expected = LINK.format(
            Site.objects.get_current().domain,
            'vocabulary',
            term.vocab_list.id,
            term.vocab_list
        )
        assert term.get_vocab() == expected


class TestProperty:
    def test_save(self):
        prop = factories.PropertyFactory.build(term_key=factories.TermFactory())
        assert Property.objects.all().count() == 0
        prop.save()
        assert Property.objects.all().count() == 1

    def test_save_strips_whitespace(self):
        vocab = factories.PropertyFactory(label=' spaces ')
        assert vocab.label == 'spaces'

    def test_get_vocab(self):
        prop = factories.PropertyFactory()
        expected = LINK.format(
            Site.objects.get_current().domain,
            'vocabulary',
            prop.term_key.vocab_list.id,
            prop.term_key.vocab_list
        )
        assert prop.get_vocab() == expected

    def test_get_term(self):
        prop = factories.PropertyFactory()
        expected = LINK.format(
            Site.objects.get_current().domain,
            'term',
            prop.term_key.id,
            prop.term_key
        )
        assert prop.get_term() == expected
