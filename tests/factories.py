"""
Factories for creating instances of Vocabulary, Term, and Property Models.
"""
from datetime import datetime

import factory
from factory import fuzzy

from controlled_vocabularies import models


class VocabularyFactory(factory.django.DjangoModelFactory):
    name = fuzzy.FuzzyText()
    label = fuzzy.FuzzyText()
    order = fuzzy.FuzzyChoice(['name', 'label', 'order'])
    maintainer = fuzzy.FuzzyChoice(['Damon', 'Gio', 'Jason', 'Lauren', 'Mark'])
    created = fuzzy.FuzzyNaiveDateTime(datetime(2012, 1, 1))
    modified = datetime.now()
    maintainerEmail = fuzzy.FuzzyText()
    definition = fuzzy.FuzzyText()

    class Meta:
        model = models.Vocabulary


class TermFactory(factory.django.DjangoModelFactory):
    vocab_list = factory.SubFactory(VocabularyFactory)
    name = fuzzy.FuzzyText(length=25)
    label = fuzzy.FuzzyText(length=120)

    class Meta:
        model = models.Term


class OrderedTermFactory(TermFactory):
    order = factory.Sequence(lambda n: str(n))


class PropertyFactory(factory.django.DjangoModelFactory):
    term_key = factory.SubFactory(TermFactory)
    property_name = fuzzy.FuzzyChoice(['definition', 'description', 'note', 'system'])
    label = fuzzy.FuzzyText()

    class Meta:
        model = models.Property
