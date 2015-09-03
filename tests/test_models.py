import pytest
from django.contrib.sites.models import Site

from controlled_vocabularies.models import Vocabulary, Term, Property


def create_vocab(name='languages', label='Language', order='name',
                 maintainer='Buddy Noone', maintainerEmail='noone@nowhere.com',
                 definition='Lorem ipsum dolor sit amet'):
    """Creates a saved instance of the Vocabulary model."""
    vocab_instance = Vocabulary(name=name,
                                label=label,
                                order=order,
                                maintainer=maintainer,
                                maintainerEmail=maintainer,
                                definition=definition)
    vocab_instance.save()
    return(vocab_instance)


def create_term(name='spanish', label='Spanish', order=2):
    """Creates a saved instance of the Term model."""
    vocab_instance = create_vocab()
    term_instance = Term(vocab_list=vocab_instance,
                         name=name,
                         label=label,
                         order=order)
    term_instance.save()
    return(term_instance)


def create_property(property_name='dialect', label='Catalan'):
    """Creates a saved instance of the Property model."""
    term_instance = create_term()
    property_instance = Property(term_key=term_instance,
                                 property_name=property_name,
                                 label=label)
    property_instance.save()
    return(property_instance)


@pytest.mark.django_db
class TestVocabulary:
    def test_save(self):
        assert Vocabulary.objects.all().count() == 0
        create_vocab()
        assert Vocabulary.objects.all().count() == 1

    def test_unicode(self):
        vocab_instance = create_vocab()
        assert unicode(vocab_instance) == 'languages'

    @pytest.mark.xfail(reason='Input is not being cleaned before being saved.')
    def test_whitespace_stripped(self):
        create_vocab(
            name=' spaces  here ',
            label=' Spaces here   too  ',
            maintainer=' Please   Fix Me ',
            maintainerEmail='  here@there.com ',
            definition='  Strip leading   and trailing, condense   others. '
        )
        vocab_from_db = Vocabulary.objects.get(pk=1)

        assert vocab_from_db.name == 'spaces here'
        assert vocab_from_db.label == 'Spaces here too'
        assert vocab_from_db.maintainer == 'Please Fix Me'
        assert vocab_from_db.maintainerEmail == 'here@there.com'
        assert vocab_from_db.definition == 'Strip leading and trailing, condense others.'


@pytest.mark.django_db
class TestTerm:
    def test_unicode(self):
        term_instance = create_term()
        assert unicode(term_instance) == 'spanish'

    def test_save(self):
        assert Term.objects.all().count() == 0
        create_term()
        assert Term.objects.all().count() == 1

    def test_get_vocab(self):
        term_instance = create_term()
        expected = "<a href='http://{}/admin/vocabularies/vocabulary/{}'>{}</a>".format(
            Site.objects.get_current().domain,
            term_instance.vocab_list.id,
            term_instance.vocab_list
        )
        assert term_instance.get_vocab() == expected

    @pytest.mark.xfail(reason='Input is not being cleaned before being saved.')
    def test_whitespace_stripped(self):
        create_term(
            name=' spaces  here ',
            label=' Spaces here   too  ',
        )
        term_from_db = Term.objects.get(pk=1)

        assert term_from_db.name == 'spaces here'
        assert term_from_db.label == 'Spaces here too'


@pytest.mark.django_db
class TestProperty:
    def test_save(self):
        assert Property.objects.all().count() == 0
        create_property()
        assert Property.objects.all().count() == 1

    def test_get_vocab(self):
        property_instance = create_property()
        expected = "<a href='http://{}/admin/vocabularies/vocabulary/{}'>{}</a>".format(
            Site.objects.get_current().domain,
            property_instance.term_key.vocab_list.id,
            property_instance.term_key.vocab_list
        )
        assert property_instance.get_vocab() == expected

    def test_get_term(self):
        property_instance = create_property()
        expected = "<a href='http://{}/admin/vocabularies/term/{}'>{}</a>".format(
            Site.objects.get_current().domain,
            property_instance.term_key.id,
            property_instance.term_key
        )
        assert property_instance.get_term() == expected

    @pytest.mark.xfail(reason='Input is not being cleaned before being saved.')
    def test_whitespace_stripped(self):
        create_property(
            property_name=' spaces  here ',
            label=' Spaces here   too  ',
        )
        property_from_db = Property.objects.get(pk=1)

        assert property_from_db.property_name == 'spaces here'
        assert property_from_db.label == 'Spaces here too'
