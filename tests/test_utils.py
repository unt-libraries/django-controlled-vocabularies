import pytest
from django.forms import ValidationError

from controlled_vocabularies import admin, views
from . import factories


@pytest.mark.django_db
def test_create_term_list():
    """Test that only the terms associated with the given vocabulary are returned."""
    vocab = factories.VocabularyFactory()
    vocab_terms = factories.TermFactory.create_batch(4, vocab_list=vocab)
    other_term = factories.TermFactory()

    term_list = views.create_term_list(vocab.id)
    for term in vocab_terms:
        assert str(term) in str(term_list)
    assert str(other_term) not in str(term_list)


def test_has_spaces_with_spaces():
    with pytest.raises(ValidationError):
        admin.has_spaces(' J o h n ')


def test_has_spaces_without_spaces():
    assert admin.has_spaces('John') == 'John'
