import pytest
from django.contrib.sites.models import Site

from controlled_vocabularies.models import Vocabulary, Term, Property


def create_vocab(name='languages', label='Language', order='name',
                 maintainer='Buddy Noone', maintainerEmail='noone@nowhere.com',
                 definition='Lorem ipsum dolor sit amet'):
    """Creates an unsaved instance of the Vocabulary model."""
    return(Vocabulary(name=name,
                      label=label,
                      order=order,
                      maintainer=maintainer,
                      maintainerEmail=maintainer,
                      definition=definition)
    )


def create_term(name='spanish', label='Spanish', order=2):
    """Creates an unsaved instance of the Term model."""
    vocab_instance = create_vocab()
    vocab_instance.save()
    return(Term(vocab_list=vocab_instance,
                name=name,
                label=label,
                order=order)
    )


def create_property(property_name='dialect', label='Catalan'):
    """Creates an unsaved instance of the Property model."""
    term_instance = create_term()
    term_instance.save()
    return(Property(term_key=term_instance,
                    property_name=property_name,
                    label=label)
    )


@pytest.mark.django_db
class TestVocabulary:
    def test_save(self):
        vocab_instance = create_vocab()
        assert Vocabulary.objects.all().count() == 0

        vocab_instance.save()
        assert Vocabulary.objects.all().count() == 1

    def test_unicode(self):
        vocab_instance = create_vocab()
        assert unicode(vocab_instance) == 'languages'


@pytest.mark.django_db
class TestTerm:
    def test_unicode(self):
        term_instance = create_term()
        assert unicode(term_instance) == 'spanish'

    def test_save(self):
        term_instance = create_term()
        assert Term.objects.all().count() == 0

        term_instance.save()
        assert Term.objects.all().count() == 1

    def test_get_vocab(self):
        term_instance = create_term()
        expected = "<a href='http://{}/admin/vocabularies/vocabulary/{}'>{}</a>".format(
                Site.objects.get_current().domain,
                term_instance.vocab_list.id,
                term_instance.vocab_list
        )
        assert term_instance.get_vocab() == expected


@pytest.mark.django_db
class TestProperty:
    def test_save(self):
        property_instance = create_property()
        assert Property.objects.all().count() == 0

        property_instance.save()
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
