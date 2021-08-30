from lxml import objectify, etree
import pytest

from controlled_vocabularies.vocabulary_handler import VocabularyHandler
from . import factories

pytestmark = pytest.mark.django_db

# Namespaces
RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
DC = 'http://purl.org/dc/elements/1.1/'
RDFS = 'http://www.w3.org/2000/01/rdf-schema#'

NS = {
    'rdf': RDF,
    'dc': DC,
    'rdfs': RDFS
}

PURL = 'http://purl.org/NET/UNTL/vocabularies/'


def test_xml_response():
    vocab = factories.VocabularyFactory()
    vocab_handler = VocabularyHandler().xml_response(vocab)
    assert vocab_handler.vocab == vocab
    assert isinstance(vocab_handler, VocabularyHandler)


@pytest.fixture
def vocab_file_xml():
    prop = factories.PropertyFactory(property_name='description')

    vocab_handler = VocabularyHandler().xml_response(prop.term_key.vocab_list)
    return prop, etree.fromstring(vocab_handler.vocab_file)


def test_create_xml_RDF_element(vocab_file_xml):
    _, root = vocab_file_xml

    assert root.tag == '{{{}}}RDF'.format(RDF)


def test_create_xml_Description_element(vocab_file_xml):
    prop, root = vocab_file_xml

    element = root.xpath('rdf:Description', namespaces=NS)[0]
    attrib = element.get('{{{}}}about'.format(RDF))
    assert attrib == PURL + prop.term_key.vocab_list.name


def test_create_xml_title_element(vocab_file_xml):
    prop, root = vocab_file_xml

    element = root.xpath('rdf:Description/dc:title', namespaces=NS)[0]
    assert element.text == prop.term_key.vocab_list.label


def test_create_xml_publisher_element(vocab_file_xml):
    _, root = vocab_file_xml

    element = root.xpath('rdf:Description/dc:publisher', namespaces=NS)[0]
    assert element.text == 'University of North Texas Libraries'


def test_create_xml_Description_subelement_description(vocab_file_xml):
    prop, root = vocab_file_xml

    element = root.xpath('rdf:Description/dc:description', namespaces=NS)[0]
    assert element.text == prop.term_key.vocab_list.definition


def test_create_xml_language_element(vocab_file_xml):
    _, root = vocab_file_xml

    element = root.xpath('rdf:Description/dc:language', namespaces=NS)[0]
    assert element.text == 'English'


def test_create_xml_date_element(vocab_file_xml):
    prop, root = vocab_file_xml

    element = root.xpath('rdf:Description/dc:date', namespaces=NS)[0]
    assert element.text == prop.term_key.vocab_list.created.strftime('%Y')


def test_create_xml_Property_element(vocab_file_xml):
    prop, root = vocab_file_xml

    element = root.xpath('rdf:Property', namespaces=NS)[0]
    attrib = element.get('{{{}}}about'.format(RDF))
    assert attrib == '{}#{}'.format(PURL + prop.term_key.vocab_list.name, prop.term_key.name)


def test_create_xml_label_element(vocab_file_xml):
    prop, root = vocab_file_xml

    element = root.xpath('rdf:Property/rdfs:label', namespaces=NS)[0]
    assert element.text == prop.term_key.label


def test_create_xml_Property_subelement_description(vocab_file_xml):
    prop, root = vocab_file_xml

    element = root.xpath('rdf:Property/dc:description', namespaces=NS)[0]
    assert element.text == prop.label


def test_create_xml_isDefinedBy_element(vocab_file_xml):
    prop, root = vocab_file_xml

    element = root.xpath('rdf:Property/rdfs:isDefinedBy', namespaces=NS)[0]
    attrib = element.get('{{{}}}resource'.format(RDF))
    assert attrib == PURL + prop.term_key.vocab_list.name


def test_py_response():
    vocab = factories.VocabularyFactory()
    vocab_handler = VocabularyHandler().py_response(vocab)
    assert vocab_handler.vocab == vocab
    assert isinstance(vocab_handler, VocabularyHandler)


def test_create_py():
    vocab_handler = VocabularyHandler().py_response(
        factories.VocabularyFactory())
    vocab_handler.create_py()
    assert vocab_handler.vocab_mimetype == 'text/plain'


def test_json_response():
    vocab = factories.VocabularyFactory()
    vocab_handler = VocabularyHandler().json_response(vocab)
    assert vocab_handler.vocab == vocab
    assert isinstance(vocab_handler, VocabularyHandler)


def test_create_json():
    vocab_handler = VocabularyHandler().json_response(
        factories.VocabularyFactory())
    vocab_handler.create_json()
    assert vocab_handler.vocab_mimetype == 'application/json'


def test_tkl_response():
    vocab = factories.VocabularyFactory()
    vocab_handler = VocabularyHandler().tkl_response(vocab)
    assert vocab_handler.vocab == vocab
    assert isinstance(vocab_handler, VocabularyHandler)


def test_create_tkl():
    """Check that the xml doc has all the expected elements, values, and attributes."""
    prop = factories.PropertyFactory(property_name='linkback')
    term = prop.term_key
    vocab = term.vocab_list

    vocab_handler = VocabularyHandler().tkl_response(vocab)

    root = objectify.fromstring(vocab_handler.vocab_file)

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
    assert b'<?xml version="1.0" encoding="UTF-8"?>' in vocab_handler.vocab_file


def test_create_tkl_order_by_name():
    vocab = factories.VocabularyFactory(order='name')
    factories.TermFactory.create_batch(4, vocab_list=vocab)
    vocab_handler = VocabularyHandler().tkl_response(vocab)

    root = objectify.fromstring(vocab_handler.vocab_file)

    sorted_terms = vocab.term_set.order_by('name')
    for actual, expected in zip(root.enum, sorted_terms):
        assert actual.get('value') == expected.name


def test_create_tkl_order_by_label():
    vocab = factories.VocabularyFactory(order='label')
    factories.TermFactory.create_batch(4, vocab_list=vocab)
    vocab_handler = VocabularyHandler().tkl_response(vocab)

    root = objectify.fromstring(vocab_handler.vocab_file)

    sorted_terms = vocab.term_set.order_by('label')
    for actual, expected in zip(root.enum, sorted_terms):
        assert actual.get('value') == expected.name


def test_create_tkl_order_by_order():
    vocab = factories.VocabularyFactory(order='order')
    factories.OrderedTermFactory.create_batch(4, vocab_list=vocab)
    vocab_handler = VocabularyHandler().tkl_response(vocab)

    root = objectify.fromstring(vocab_handler.vocab_file)

    sorted_terms = vocab.term_set.order_by('order', 'name')
    for actual, expected in zip(root.enum, sorted_terms):
        assert actual.get('value') == expected.name


def test_create_vocab_dict():
    # Create a vocab, term, and property that should be in the vocab_dict.
    prop = factories.PropertyFactory()
    vocab = prop.term_key.vocab_list

    vocab_handler = VocabularyHandler().py_response(vocab)
    vocab_dict = vocab_handler.create_vocab_dict('py')

    assert vocab_dict['name'] == vocab.name
    assert vocab_dict['label'] == vocab.label
    assert vocab_dict['order'] == vocab.order
    assert vocab_dict['maintainerEmail'] == vocab.maintainerEmail
    assert vocab_dict['definition'] == vocab.definition
    assert vocab_dict['created'] == vocab.created
    assert vocab_dict['modified'] == vocab.modified
    assert 'terms' in vocab_dict.keys()


def test_create_vocab_dict_term_sub_dict():
    """Test that the embedded dictionary contains the right information."""
    prop = factories.PropertyFactory()
    term = prop.term_key
    vocab = term.vocab_list

    vocab_handler = VocabularyHandler().py_response(vocab)
    vocab_dict = vocab_handler.create_vocab_dict('py')

    term_dict = vocab_dict['terms'][0]
    assert term_dict['name'] == term.name
    assert term_dict['label'] == term.label
    assert term_dict['order'] == term.order
    assert term_dict['url'] == 'http://purl.org/NET/UNTL/vocabularies/{}/#{}'.format(
        vocab.name, term.name)
    assert 'properties' in term_dict


def test_create_vocab_dict_properties_sub_dict():
    """Test that the embedded dictionary contains the right information."""
    prop = factories.PropertyFactory()

    vocab_handler = VocabularyHandler().py_response(prop.term_key.vocab_list)
    vocab_dict = vocab_handler.create_vocab_dict('py')

    prop_dict = vocab_dict['terms'][0]['properties'][0]
    assert prop_dict['property_name'] == prop.property_name
    assert prop_dict['label'] == prop.label


def test_create_vocab_dict_format_py():
    prop = factories.PropertyFactory()
    vocab = prop.term_key.vocab_list

    vocab_handler = VocabularyHandler().py_response(vocab)
    vocab_dict = vocab_handler.create_vocab_dict('py')

    assert vocab_dict['created'] == vocab.created
    assert vocab_dict['modified'] == vocab.modified


def test_create_vocab_dict_format_json():
    prop = factories.PropertyFactory()
    vocab = prop.term_key.vocab_list

    vocab_handler = VocabularyHandler().py_response(vocab)
    vocab_dict = vocab_handler.create_vocab_dict('json')

    assert vocab_dict['created'] == str(vocab.created)
    assert vocab_dict['modified'] == str(vocab.modified)
