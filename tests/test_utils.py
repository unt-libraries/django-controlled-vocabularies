from lxml import objectify
import pytest
from django.forms import ValidationError

from controlled_vocabularies import admin, views
from controlled_vocabularies.vocabulary_handler import VocabularyHandler
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


@pytest.mark.django_db
class TestVocabularyHandler():

    def test_xml_response(self):
        vocab = factories.VocabularyFactory()
        vocab_handler = VocabularyHandler().xml_response(vocab)
        assert vocab_handler.vocab == vocab
        assert isinstance(vocab_handler, VocabularyHandler)

    def test_create_xml(self):
        # XML namespaces.
        rdf_ns = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
        dc_ns = '{http://purl.org/dc/elements/1.1/}'
        rdfs_ns = '{http://www.w3.org/2000/01/rdf-schema#}'

        prop = factories.PropertyFactory(property_name='definition')
        term = prop.term_key
        vocab = term.vocab_list

        vocab_handler = VocabularyHandler().xml_response(vocab)

        # Check that all the expected elements are in the vocab_list attribute and that they
        # have the expected values and attributes.
        root = objectify.fromstring(vocab_handler.vocab_file)
        assert root.tag == '{}RDF'.format(rdf_ns)
        rdf_description = root['{}Description'.format(rdf_ns)]
        assert rdf_description.get('{}about'.format(rdf_ns)) == (
            'http://purl.org/NET/UNTL/vocabularies/formats/')
        assert rdf_description['{}title'.format(dc_ns)] == vocab.label
        assert rdf_description['{}publisher'.format(dc_ns)] == (
            'University of North Texas Libraries')
        assert rdf_description['{}description'.format(dc_ns)] == vocab.definition
        assert rdf_description['{}language'.format(dc_ns)] == 'English'
        assert str(rdf_description['{}date'.format(dc_ns)]) == vocab.created.strftime('%Y')
        rdf_property = root['{}Property'.format(rdf_ns)]
        assert rdf_property.get('{}about'.format(rdf_ns)) == (
            'http://purl.org/NET/UNTL/vocabularies/formats/#{}'.format(term.name))
        assert rdf_property['{}label'.format(rdfs_ns)] == term.label
        assert rdf_property['{}description'.format(dc_ns)] == prop.label
        assert rdf_property['{}isDefinedBy'.format(rdfs_ns)].get('{}resource'.format(rdf_ns)) == (
            'http://purl.org/NET/UNTL/vocabularies/formats/')
        assert vocab_handler.vocab_mimetype == 'text/xml'
        assert '<?xml version="1.0" encoding="UTF-8"?>' in vocab_handler.vocab_file

    def test_py_response(self):
        vocab = factories.VocabularyFactory()
        vocab_handler = VocabularyHandler().py_response(vocab)
        assert vocab_handler.vocab == vocab
        assert isinstance(vocab_handler, VocabularyHandler)

    def test_create_py(self):
        vocab_handler = VocabularyHandler().py_response(
            factories.VocabularyFactory())
        vocab_handler.create_py()
        assert vocab_handler.vocab_mimetype == 'text/plain'

    def test_json_response(self):
        vocab = factories.VocabularyFactory()
        vocab_handler = VocabularyHandler().json_response(vocab)
        assert vocab_handler.vocab == vocab
        assert isinstance(vocab_handler, VocabularyHandler)

    def test_create_json(self):
        vocab_handler = VocabularyHandler().json_response(
            factories.VocabularyFactory())
        vocab_handler.create_json()
        assert vocab_handler.vocab_mimetype == 'application/json'

    def test_tkl_response(self):
        vocab = factories.VocabularyFactory()
        vocab_handler = VocabularyHandler().tkl_response(vocab)
        assert vocab_handler.vocab == vocab
        assert isinstance(vocab_handler, VocabularyHandler)

    def test_create_tkl(self):
        prop = factories.PropertyFactory(property_name='linkback')
        term = prop.term_key
        vocab = term.vocab_list

        vocab_handler = VocabularyHandler().tkl_response(vocab)

        root = objectify.fromstring(vocab_handler.vocab_file)

        # Check that the xml doc has all the expected elements, values, and attributes.
        assert root.tag == 'authority'
        assert root.get('creator') == vocab.maintainer
        assert root.get('created') == str(vocab.created).replace(' ', ', ')
        assert root.get('modifier') == vocab.maintainer
        assert root.get('modified') == str(vocab.modified).replace(' ', ', ')
        assert root.enum.get('value') == term.name
        assert root.enum.get('order') == '1'
        assert root.enum.string.get('{http://www.w3.org/XML/1998/namespace}lang') == 'en'
        assert root.enum.string == term.label
        assert root.enum.linkback == prop.label
        assert vocab_handler.vocab_mimetype == 'text/xml'
        assert '<?xml version="1.0" encoding="UTF-8"?>' in vocab_handler.vocab_file

    def test_create_tkl_order_by_name(self):
        vocab = factories.VocabularyFactory(order='name')
        factories.TermFactory.create_batch(4, vocab_list=vocab)
        vocab_handler = VocabularyHandler().tkl_response(vocab)

        root = objectify.fromstring(vocab_handler.vocab_file)

        sorted_terms = vocab.term_set.order_by('name')
        for actual, expected in zip(root.enum, sorted_terms):
            assert actual.get('value') == expected.name

    def test_create_tkl_order_by_label(self):
        vocab = factories.VocabularyFactory(order='label')
        factories.TermFactory.create_batch(4, vocab_list=vocab)
        vocab_handler = VocabularyHandler().tkl_response(vocab)

        root = objectify.fromstring(vocab_handler.vocab_file)

        sorted_terms = vocab.term_set.order_by('label')
        for actual, expected in zip(root.enum, sorted_terms):
            assert actual.get('value') == expected.name

    def test_create_tkl_order_by_order(self):
        vocab = factories.VocabularyFactory(order='order')
        factories.OrderedTermFactory.create_batch(4, vocab_list=vocab)
        vocab_handler = VocabularyHandler().tkl_response(vocab)

        root = objectify.fromstring(vocab_handler.vocab_file)

        sorted_terms = vocab.term_set.order_by('order', 'name')
        for actual, expected in zip(root.enum, sorted_terms):
            assert actual.get('value') == expected.name

    def test_create_vocab_dict(self):
        # Create a vocab, term, and property that should be in the vocab_dict.
        prop = factories.PropertyFactory()
        term = prop.term_key
        vocab = term.vocab_list

        vocab_handler = VocabularyHandler().py_response(vocab)
        vocab_dict = vocab_handler.create_vocab_dict('py')

        assert vocab_dict['name'] == vocab.name
        assert vocab_dict['label'] == vocab.label
        assert vocab_dict['order'] == vocab.order
        assert vocab_dict['maintainerEmail'] == vocab.maintainerEmail
        assert vocab_dict['definition'] == vocab.definition
        assert vocab_dict['created'] == vocab.created
        assert vocab_dict['modified'] == vocab.modified
        assert vocab_dict['terms'] == [{
            'name': term.name,
            'label': term.label,
            'order': term.order,
            'url': 'http://purl.org/NET/UNTL/vocabularies/{}/#{}'.format(
                vocab.name,
                term.name),
            'properties': [{
                'property_name': prop.property_name,
                'label': prop.label
            }, ]
        }, ]

    def test_create_vocab_dict_format_py(self):
        prop = factories.PropertyFactory()
        vocab = prop.term_key.vocab_list

        vocab_handler = VocabularyHandler().py_response(vocab)
        vocab_dict = vocab_handler.create_vocab_dict('py')

        assert vocab_dict['created'] == vocab.created
        assert vocab_dict['modified'] == vocab.modified

    def test_create_vocab_dict_format_json(self):
        prop = factories.PropertyFactory()
        vocab = prop.term_key.vocab_list

        vocab_handler = VocabularyHandler().py_response(vocab)
        vocab_dict = vocab_handler.create_vocab_dict('json')

        assert vocab_dict['created'] == str(vocab.created)
        assert vocab_dict['modified'] == str(vocab.modified)
