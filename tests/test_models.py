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

    def test_unicode(self):
        vocab = factories.VocabularyFactory()
        assert unicode(vocab) == vocab.name

    @pytest.mark.xfail(reason='Input is not being cleaned before being saved.')
    def test_whitespace_stripped(self):
        factories.VocabularyFactory(
            name=' spaces  here ',
            label=' Spaces here   too  ',
            maintainer=' Please   Fix Me ',
            maintainerEmail='  here@there.com ',
            definition='  Strip leading   and trailing, condense   others. '
        )
        vocab = Vocabulary.objects.get(pk=1)

        assert vocab.name == 'spaces here'
        assert vocab.label == 'Spaces here too'
        assert vocab.maintainer == 'Please Fix Me'
        assert vocab.maintainerEmail == 'here@there.com'
        assert vocab.definition == 'Strip leading and trailing, condense others.'


class TestTerm:
    def test_unicode(self):
        term = factories.TermFactory()
        assert unicode(term) == term.name

    def test_save(self):
        term = factories.TermFactory.build(vocab_list=factories.VocabularyFactory())
        assert Term.objects.all().count() == 0
        term.save()
        assert Term.objects.all().count() == 1

    def test_get_vocab(self):
        term = factories.TermFactory()
        expected = LINK.format(
            Site.objects.get_current().domain,
            'vocabulary',
            term.vocab_list.id,
            term.vocab_list
        )
        assert term.get_vocab() == expected

    @pytest.mark.xfail(reason='Input is not being cleaned before being saved.')
    def test_whitespace_stripped(self):
        factories.TermFactory(
            name=' spaces  here ',
            label=' Spaces here   too  ',
        )
        term = Term.objects.get(pk=1)

        assert term.name == 'spaces here'
        assert term.label == 'Spaces here too'


class TestProperty:
    def test_save(self):
        prop = factories.PropertyFactory.build(term_key=factories.TermFactory())
        assert Property.objects.all().count() == 0
        prop.save()
        assert Property.objects.all().count() == 1

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

    @pytest.mark.xfail(reason='Input is not being cleaned before being saved.')
    def test_whitespace_stripped(self):
        factories.PropertyFactory(
            property_name=' spaces  here ',
            label=' Spaces here   too  ',
        )
        prop = Property.objects.get(pk=1)

        assert prop.property_name == 'spaces here'
        assert prop.label == 'Spaces here too'
