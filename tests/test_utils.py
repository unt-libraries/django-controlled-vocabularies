import pytest
from django.forms import ValidationError

from controlled_vocabularies.admin import has_spaces


@pytest.mark.django_db
def test_create_term_list():
    pass


def test_has_spaces_with_spaces():
    with pytest.raises(ValidationError):
        has_spaces(' J o h n ')


def test_has_spaces_without_spaces():
    assert has_spaces('John') == 'John'


class TestVocabularyHandler():

    def test_xml_response(self):
        pass

    def test_create_xml(self):
        pass

    def test_py_response(self):
        pass

    def test_create_py(self):
        pass

    def test_json_response(self):
        pass

    def test_create_json(self):
        pass

    def test_tkl_response(self):
        pass

    def test_create_tkl(self):
        pass

    def test_create_vocab_dict(self):
        pass
