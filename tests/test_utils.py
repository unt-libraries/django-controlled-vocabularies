from datetime import datetime

from lxml import etree, objectify
import pytest
from django.forms import ValidationError

from controlled_vocabularies import admin, views, vocabulary_handler
from factories import PropertyFactory, TermFactory, VocabularyFactory, OrderedTermFactory


@pytest.mark.django_db
def test_create_term_list():
    """Test that only the terms associated with the given vocabulary are returned."""
    vocab = VocabularyFactory()
    vocab_terms = TermFactory.create_batch(4, vocab_list=vocab)
    other_term = TermFactory()

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
        vocab = VocabularyFactory()
        vocab_handler = vocabulary_handler.VocabularyHandler().xml_response(vocab)
        assert vocab_handler.vocab == vocab
        assert isinstance(vocab_handler, vocabulary_handler.VocabularyHandler)

    def test_create_xml(self):
        rdf_ns = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
        dc_ns = '{http://purl.org/dc/elements/1.1/}'
        rdfs_ns = '{http://www.w3.org/2000/01/rdf-schema#}'

        targeted = PropertyFactory(property_name='definition')

        vocab_handler = vocabulary_handler.VocabularyHandler().xml_response(
                targeted.term_key.vocab_list)

        root = objectify.fromstring(vocab_handler.vocab_file)
        assert root.tag == '{}RDF'.format(rdf_ns)
        rdf_description = root['{}Description'.format(rdf_ns)]
        assert rdf_description.get('{}about'.format(rdf_ns)) == ('http://purl.org/NET/UNTL/'
                'vocabularies/formats/')
        dc_title = rdf_description['{}title'.format(dc_ns)]
        assert dc_title == targeted.term_key.vocab_list.label
        dc_publisher = rdf_description['{}publisher'.format(dc_ns)]
        assert dc_publisher == 'University of North Texas Libraries'
        dc_description = rdf_description['{}description'.format(dc_ns)]
        assert dc_description == targeted.term_key.vocab_list.definition
        dc_language = rdf_description['{}language'.format(dc_ns)]
        assert dc_language == 'English'
        dc_date = rdf_description['{}date'.format(dc_ns)]
        assert str(dc_date) == targeted.term_key.vocab_list.created.strftime('%Y')
        rdf_property = root['{}Property'.format(rdf_ns)]
        assert rdf_property.get('{}about'.format(rdf_ns)) == ('http://purl.org/NET/UNTL/'
                'vocabularies/formats/#{}'.format(targeted.term_key.name))
        rdfs_label = rdf_property['{}label'.format(rdfs_ns)]
        assert rdfs_label == targeted.term_key.label
        prop_dc_description = rdf_property['{}description'.format(dc_ns)]
        assert prop_dc_description == targeted.label
        rdfs_isDefinedBy = rdf_property['{}isDefinedBy'.format(rdfs_ns)]
        assert rdfs_isDefinedBy.get('{}resource'.format(rdf_ns)) == ('http://purl.org/NET/UNTL/'
                'vocabularies/formats/')

    def test_py_response(self):
        vocab = VocabularyFactory()
        vocab_handler = vocabulary_handler.VocabularyHandler().py_response(vocab)
        assert vocab_handler.vocab == vocab
        assert isinstance(vocab_handler, vocabulary_handler.VocabularyHandler)

    def test_create_py(self):
        vocab_handler = vocabulary_handler.VocabularyHandler().py_response(VocabularyFactory())
        vocab_handler.create_py()
        assert vocab_handler.vocab_mimetype == 'text/plain'

    def test_json_response(self):
        vocab = VocabularyFactory()
        vocab_handler = vocabulary_handler.VocabularyHandler().json_response(vocab)
        assert vocab_handler.vocab == vocab
        assert isinstance(vocab_handler, vocabulary_handler.VocabularyHandler)

    def test_create_json(self):
        vocab_handler = vocabulary_handler.VocabularyHandler().json_response(VocabularyFactory())
        vocab_handler.create_json()
        assert vocab_handler.vocab_mimetype == 'application/json'

    def test_tkl_response(self):
        vocab = VocabularyFactory()
        vocab_handler = vocabulary_handler.VocabularyHandler().tkl_response(vocab)
        assert vocab_handler.vocab == vocab
        assert isinstance(vocab_handler, vocabulary_handler.VocabularyHandler)

    def test_create_tkl(self):
        targeted = PropertyFactory(property_name='linkback')
        vocab_handler = vocabulary_handler.VocabularyHandler().tkl_response(
                targeted.term_key.vocab_list)
        
        root = objectify.fromstring(vocab_handler.vocab_file)
        assert root.tag == 'authority'
        assert root.get('creator') == targeted.term_key.vocab_list.maintainer
        assert root.get('created') == str(targeted.term_key.vocab_list.created).replace(' ', ', ')
        assert root.get('modifier') == targeted.term_key.vocab_list.maintainer
        assert root.get('modified') == str(targeted.term_key.vocab_list.modified).replace(' ',
                                                                                          ', ')
        assert root.enum.get('value') == targeted.term_key.name
        assert root.enum.get('order') == '1'
        assert root.enum.string.get('{http://www.w3.org/XML/1998/namespace}lang') == 'en'
        assert root.enum.string == targeted.term_key.label
        assert root.enum.linkback == targeted.label
        assert vocab_handler.vocab_mimetype == 'text/xml'
        assert '<?xml version="1.0" encoding="UTF-8"?>' in vocab_handler.vocab_file
        
    def test_create_tkl_order_by_name(self):
        vocab = VocabularyFactory(order='name')
        terms = TermFactory.create_batch(4, vocab_list=vocab)
        vocab_handler = vocabulary_handler.VocabularyHandler().tkl_response(vocab)

        root = objectify.fromstring(vocab_handler.vocab_file)

        sorted_terms = vocab.term_set.order_by('name')
        for i in range(4):
            assert root.enum[i].get('value') == sorted_terms[i].name

    def test_create_tkl_order_by_label(self):
        vocab = VocabularyFactory(order='label')
        terms = TermFactory.create_batch(4, vocab_list=vocab)
        vocab_handler = vocabulary_handler.VocabularyHandler().tkl_response(vocab)

        root = objectify.fromstring(vocab_handler.vocab_file)

        sorted_terms = vocab.term_set.order_by('label')
        for i in range(4):
            assert root.enum[i].get('value') == sorted_terms[i].name

    def test_create_tkl_order_by_order(self):
        vocab = VocabularyFactory(order='order')
        terms = OrderedTermFactory.create_batch(4, vocab_list=vocab)
        vocab_handler = vocabulary_handler.VocabularyHandler().tkl_response(vocab)

        root = objectify.fromstring(vocab_handler.vocab_file)

        sorted_terms = vocab.term_set.order_by('order', 'name')
        for i in range(4):
            assert root.enum[i].get('value') == sorted_terms[i].name

    def test_create_vocab_dict(self):
        # Create a vocab, term, and property that should be in the vocab_dict.
        targeted = PropertyFactory()
        
        vocab_handler = vocabulary_handler.VocabularyHandler().py_response(
                targeted.term_key.vocab_list)
        vocab_dict = vocab_handler.create_vocab_dict('py')

        assert vocab_dict['name'] == targeted.term_key.vocab_list.name
        assert vocab_dict['label'] == targeted.term_key.vocab_list.label
        assert vocab_dict['order'] == targeted.term_key.vocab_list.order
        assert vocab_dict['maintainerEmail'] == targeted.term_key.vocab_list.maintainerEmail
        assert vocab_dict['definition'] == targeted.term_key.vocab_list.definition
        assert vocab_dict['created'] == targeted.term_key.vocab_list.created
        assert vocab_dict['modified'] == targeted.term_key.vocab_list.modified
        assert vocab_dict['terms'] == [{
            'name': targeted.term_key.name,
            'label': targeted.term_key.label,
            'order': targeted.term_key.order,
            'url': 'http://purl.org/NET/UNTL/vocabularies/{}/#{}'.format(
                targeted.term_key.vocab_list.name,
                targeted.term_key.name),
            'properties': [{
                'property_name': targeted.property_name,
                'label': targeted.label
            }, ]
        }, ]

    def test_create_vocab_dict_format_py(self):
        targeted = PropertyFactory()
        
        vocab_handler = vocabulary_handler.VocabularyHandler().py_response(
                targeted.term_key.vocab_list)
        vocab_dict = vocab_handler.create_vocab_dict('py')

        assert vocab_dict['created'] == targeted.term_key.vocab_list.created
        assert vocab_dict['modified'] == targeted.term_key.vocab_list.modified

    def test_create_vocab_dict_format_json(self):
        targeted = PropertyFactory()
        
        vocab_handler = vocabulary_handler.VocabularyHandler().py_response(
                targeted.term_key.vocab_list)
        vocab_dict = vocab_handler.create_vocab_dict('json')

        assert vocab_dict['created'] == str(targeted.term_key.vocab_list.created)
        assert vocab_dict['modified'] == str(targeted.term_key.vocab_list.modified)
