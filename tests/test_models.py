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
        vocab = factories.VocabularyFactory(
            name=' spaces  here ',
            label=' Spaces here   too  ',
            maintainer=' Please   Fix Me ',
            maintainerEmail='  here@there.com ',
            definition='  Strip leading   and trailing, condense   others. '
        )
        updated_vocab = Vocabulary.objects.get(pk=vocab.pk)

        assert updated_vocab.name == 'spaces here'
        assert updated_vocab.label == 'Spaces here too'
        assert updated_vocab.maintainer == 'Please Fix Me'
        assert updated_vocab.maintainerEmail == 'here@there.com'
        assert updated_vocab.definition == 'Strip leading and trailing, condense others.'


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
        term = factories.TermFactory(
            name=' spaces  here ',
            label=' Spaces here   too  ',
        )
        updated_term = Term.objects.get(pk=term.pk)

        assert updated_term.name == 'spaces here'
        assert updated_term.label == 'Spaces here too'


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
        prop = factories.PropertyFactory(
            property_name=' spaces  here ',
            label=' Spaces here   too  ',
        )
        updated_prop = Property.objects.get(pk=prop)

        assert updated_prop.property_name == 'spaces here'
        assert updated_prop.label == 'Spaces here too'
