import pytest
from django.contrib.sites.models import Site

from controlled_vocabularies.models import Vocabulary, Term, Property


@pytest.mark.django_db
class TestVocabulary:
    def test_save(self):
        vocab_instance = Vocabulary(
                name='languages',
                label='Lanugage',
                order='name',
                maintainer='Buddy Noone',
                maintainerEmail='noone@nowhere.com',
                definition='Lorem ipsum dolor sit amet, consectetur adipiscing elt.'
        )

        assert Vocabulary.objects.all().count() == 0
        vocab_instance.save()
        assert Vocabulary.objects.all().count() == 1

    def test_unicode(self):
        vocab_instance = Vocabulary(
                name='languages',
                label='Lanugage',
                order='name',
                maintainer='Buddy Noone',
                maintainerEmail='noone@nowhere.com',
                definition='Lorem ipsum dolor sit amet, consectetur adipiscing elt.'
        )

        assert unicode(vocab_instance) == 'languages'


@pytest.mark.django_db
class TestTerm:

    def test_unicode(self):
        vocab_instance = Vocabulary(
                name='languages',
                label='Lanugage',
                order='name',
                maintainer='Buddy Noone',
                maintainerEmail='noone@nowhere.com',
                definition='Lorem ipsum dolor sit amet, consectetur adipiscing elt.'
        )
        vocab_instance.save()
        term_instance = Term(
                vocab_list=vocab_instance,
                name='spanish',
                label='Spanish',
                order=2
        )

        assert unicode(term_instance) == 'spanish'

    def test_save(self):
        vocab_instance = Vocabulary(
                name='languages',
                label='Lanugage',
                order='name',
                maintainer='Buddy Noone',
                maintainerEmail='noone@nowhere.com',
                definition='Lorem ipsum dolor sit amet, consectetur adipiscing elt.'
        )
        vocab_instance.save()
        term_instance = Term(
                vocab_list=vocab_instance,
                name='spanish',
                label='Spanish',
                order=2
        )

        assert Term.objects.all().count() == 0
        term_instance.save()
        assert Term.objects.all().count() == 1

    def test_get_vocab(self):
        vocab_instance = Vocabulary(
                name='languages',
                label='Lanugage',
                order='name',
                maintainer='Buddy Noone',
                maintainerEmail='noone@nowhere.com',
                definition='Lorem ipsum dolor sit amet, consectetur adipiscing elt.'
        )
        vocab_instance.save()
        term_instance = Term(
                vocab_list=vocab_instance,
                name='spanish',
                label='Spanish',
                order=2
        )

        expected = "<a href='http://{}/admin/vocabularies/vocabulary/{}'>{}</a>".format(
                Site.objects.get_current().domain,
                term_instance.vocab_list.id,
                term_instance.vocab_list
        )

        assert term_instance.get_vocab() == expected


@pytest.mark.django_db
class TestProperty:
    def test_save(self):
        vocab_instance = Vocabulary(
                name='languages',
                label='Lanugage',
                order='name',
                maintainer='Buddy Noone',
                maintainerEmail='noone@nowhere.com',
                definition='Lorem ipsum dolor sit amet, consectetur adipiscing elt.'
        )
        vocab_instance.save()
        term_instance = Term(
                vocab_list=vocab_instance,
                name='spanish',
                label='Spanish',
                order=2
        )
        term_instance.save()
        property_instance = Property(
                term_key=term_instance,
                property_name='dialect',
                label='Catalan'
        )

        assert Property.objects.all().count() == 0
        property_instance.save()
        assert Property.objects.all().count() == 1


    def test_get_vocab(self):
        vocab_instance = Vocabulary(
                name='languages',
                label='Lanugage',
                order='name',
                maintainer='Buddy Noone',
                maintainerEmail='noone@nowhere.com',
                definition='Lorem ipsum dolor sit amet, consectetur adipiscing elt.'
        )
        vocab_instance.save()
        term_instance = Term(
                vocab_list=vocab_instance,
                name='spanish',
                label='Spanish',
                order=2
        )
        term_instance.save()
        property_instance = Property(
                term_key=term_instance,
                property_name='dialect',
                label='Catalan'
        )

        expected = "<a href='http://{}/admin/vocabularies/vocabulary/{}'>{}</a>".format(
                Site.objects.get_current().domain,
                property_instance.term_key.vocab_list.id,
                property_instance.term_key.vocab_list
        )

        assert property_instance.get_vocab() == expected

    def test_get_term(self):
        vocab_instance = Vocabulary(
                name='languages',
                label='Lanugage',
                order='name',
                maintainer='Buddy Noone',
                maintainerEmail='noone@nowhere.com',
                definition='Lorem ipsum dolor sit amet, consectetur adipiscing elt.'
        )
        vocab_instance.save()
        term_instance = Term(
                vocab_list=vocab_instance,
                name='spanish',
                label='Spanish',
                order=2
        )
        term_instance.save()
        property_instance = Property(
                term_key=term_instance,
                property_name='dialect',
                label='Catalan'
        )

        expected = "<a href='http://{}/admin/vocabularies/term/{}'>{}</a>".format(
                Site.objects.get_current().domain,
                property_instance.term_key.id,
                property_instance.term_key
        )

        assert property_instance.get_term() == expected
