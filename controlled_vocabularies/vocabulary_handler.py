# Don't forget to install elementtree, simplejson on whatever server you deploy this on
from lxml.etree import Element, SubElement, tostring, register_namespace
import json
from controlled_vocabularies.models import Term, Property
from django.conf import settings


class VocabularyHandler:

    # XML Handler
    @classmethod
    def xml_response(cls, vocab):
        c = cls()
        c.vocab = vocab
        c.create_xml()

        # Returns the instance object of the datastructure
        return c

    def create_xml(c):
        # Define urls for schemas
        rdf_url = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
        dc_url = 'http://purl.org/dc/elements/1.1/'
        rdfs_url = 'http://www.w3.org/2000/01/rdf-schema#'
        # Define Namespaces
        rdf_namespace = "{%s}" % (rdf_url)
        dc_namespace = "{%s}" % (dc_url)
        rdfs_namespace = "{%s}" % (rdfs_url)
        purl_namespace = 'http://purl.org/NET/UNTL/vocabularies/formats/'
        # Define Static Attributes
        isDefinedBy_attribs = {'{%s}resource' % rdf_url: purl_namespace}
        # Root
        root = Element(
            rdf_namespace + 'RDF',
            nsmap={
                'rdfs': rdfs_url,
                'rdf': rdf_url,
                'dc': dc_url,
                'dcq': 'http://purl.org/dc/terms/',
            },
        )
        # RDF Description
        register_namespace('rdf', 'rdf:about')
        rdf_description = SubElement(
            root,
            '{%s}Description' % rdf_url,
            {'{%s}about' % rdf_url: purl_namespace}
        )
        # DC Title
        dc_title = SubElement(rdf_description, dc_namespace+'title')
        dc_title.text = c.vocab.label
        # DC Publisher
        dc_publisher = SubElement(rdf_description, dc_namespace+'publisher')
        dc_publisher.text = 'University of North Texas Libraries'
        # DC Description
        dc_description = SubElement(rdf_description, dc_namespace+'description')
        dc_description.text = c.vocab.definition
        # DC Language
        dc_language = SubElement(rdf_description, dc_namespace+'language')
        dc_language.text = 'English'
        # DC Date
        dc_date = SubElement(rdf_description, dc_namespace+'date')
        dc_date.text = str(c.vocab.created.strftime("%Y"))

        for term in Term.objects.filter(vocab_list=c.vocab.id):
            # RDF Property
            property_attribs = {'{%s}about' % rdf_url: purl_namespace+'#'+term.name}
            rdf_property = SubElement(
                root,
                rdf_namespace+'Property',
                property_attribs
            )
            # RDFS Label
            rdfs_label = SubElement(rdf_property, rdfs_namespace+'label')
            rdfs_label.text = term.label
            for prop in Property.objects.filter(term_key=term.id):
                # DC Description
                if prop.property_name == 'definition':
                    prop_dc_description = SubElement(rdf_property, dc_namespace+'description')
                    prop_dc_description.text = prop.label
            # RDFS isDefinedBy
            SubElement(
                rdf_property,
                rdfs_namespace+'isDefinedBy',
                isDefinedBy_attribs
            )

        # File and Mimetype
        c.vocab_mimetype = 'text/xml'
        c.vocab_file = '<?xml version="1.0" encoding="UTF-8"?>'+tostring(root)

    # Python Handler
    @classmethod
    def py_response(cls, vocab):
        c = cls()
        c.vocab = vocab
        c.create_py()

        # Returns the instance object of the datastructure
        return c

    def create_py(c):
        # File and Mimetype
        c.vocab_mimetype = 'text/plain'
        c.vocab_file = str(c.create_vocab_dict('py'))

    # JSON Handler
    @classmethod
    def json_response(cls, vocab):
        c = cls()
        c.vocab = vocab
        c.create_json()

        # Returns the instance object of the datastructure
        return c

    def create_json(c):
        # File and Mimetype
        c.vocab_mimetype = 'application/json'
        c.vocab_file = json.dumps(c.create_vocab_dict('json'))

    # TKL Handler
    @classmethod
    def tkl_response(cls, vocab):
        c = cls()
        c.vocab = vocab
        c.create_tkl()

        # Returns the instance object of the datastructure
        return c

    def create_tkl(c):
        current_order = 1
        # Fix time formating
        created_string = str(c.vocab.created).replace(' ', ', ')
        modified_string = str(c.vocab.modified).replace(' ', ', ')
        # Define static attributes
        auth_attribs = {'creator': c.vocab.maintainer, 'created': created_string,
                        'modifier': c.vocab.maintainer, 'modified': modified_string}
        # used to look like this:
        # string_attribs = {'xml:lang': 'en'}
        # string_attribs = {'lang': 'en'}
        xmlns = "http://www.w3.org/XML/1998/namespace"
        string_attribs = {"{%s}lang" % xmlns: "en"}
        root = Element('authority', auth_attribs)
        # Sort Terms by order field
        if c.vocab.order == 'name':
            term_list = Term.objects.filter(vocab_list=c.vocab.id).order_by('name')
        elif c.vocab.order == 'label':
            term_list = Term.objects.filter(vocab_list=c.vocab.id).order_by('label')
        elif c.vocab.order == 'order':
            term_list = Term.objects.filter(vocab_list=c.vocab.id).order_by('order', 'name')

        for term in term_list:
            # Automatically generate an order value
            enum_attribs = {'value': term.name, 'order': str(current_order)}
            # Enum
            sub_enum = SubElement(root, 'enum', enum_attribs)
            # String
            sub_string = SubElement(sub_enum, 'string', string_attribs)
            sub_string.text = term.label
            for prop in Property.objects.filter(term_key=term.id):
                # Linkback
                if prop.property_name == 'linkback':
                    sub_linkback = SubElement(sub_enum, 'linkback')
                    sub_linkback.text = prop.label
            current_order += 1
        # File and Mimetype
        c.vocab_mimetype = 'text/xml'
        c.vocab_file = '<?xml version="1.0" encoding="UTF-8"?>'+tostring(root)

    def create_vocab_dict(c, format):
        # Create the vocabulary base url
        vocabulary_url = "%svocabularies/%s/" % (settings.VOCAB_DOMAIN, c.vocab.name)
        # Generate the Vocabulary Dictionary
        vocab_dict = {"name": c.vocab.name, "label": c.vocab.label,
                      "maintainer": c.vocab.maintainer, "order": c.vocab.order,
                      "maintainerEmail": c.vocab.maintainerEmail,
                      "definition": c.vocab.definition}
        if format == 'py':
            vocab_dict['created'] = c.vocab.created
            vocab_dict['modified'] = c.vocab.modified
        elif format == 'json':
            vocab_dict['created'] = str(c.vocab.created)
            vocab_dict['modified'] = str(c.vocab.modified)
        term_list = []
        for term in Term.objects.filter(vocab_list=c.vocab.id):
            term_dict = {}
            term_url = "%s#%s" % (vocabulary_url, term.name)
            # Generate the Term Dictionary
            term_dict = {
                "name": term.name,
                "label": term.label,
                "order": term.order,
                "url": term_url,
                }
            prop_list = []
            for prop in Property.objects.filter(term_key=term.id):
                prop_dict = {}
                # Generate the Property Dictionary
                prop_dict = {"property_name": prop.property_name,
                             "label": prop.label}
                # Add the individual Property dict to the Property list
                prop_list.append(prop_dict)
            # Add the Property list to the Term dict
            term_dict['properties'] = prop_list
            # Add the individual Term dict to the Term list
            term_list.append(term_dict)
        # Add the Term list to the Property dict
        vocab_dict['terms'] = term_list

        return vocab_dict
