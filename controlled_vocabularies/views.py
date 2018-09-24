import string
from django import http
from controlled_vocabularies.models import Vocabulary, Term, Property
from django.http import HttpResponse
from django.shortcuts import render
from controlled_vocabularies.vocabulary_handler import VocabularyHandler
from django.conf import settings


def about(request):
    return render(
        request,
        'vocabularies/about.html',
    )


# Function to create a Term list using the vocab id # NOT A VIEW #
def create_term_list(vocab_id):
    term_list = []
    vocab = Vocabulary.objects.get(id=vocab_id)
    vocab_terms = Term.objects.filter(vocab_list=vocab_id).order_by(vocab.order, 'name')
    for t in vocab_terms:
        term_dict = {}
        term_dict['term_item'] = t
        term_dict['properties'] = Property.objects.filter(term_key=t.id)
        term_list.append(term_dict)

    return term_list


def vocabulary_list(request):
    return render(
        request,
        'vocabularies/vocabulary_list.html',
        {'vocabularies': Vocabulary.objects.all().order_by('name')},
    )


def term_list(request, vocabulary_name):
    try:
        vocab_object = Vocabulary.objects.get(name__exact=vocabulary_name)
    except(Vocabulary.DoesNotExist, Vocabulary.MultipleObjectsReturned):
        raise http.Http404
    term_list = create_term_list(vocab_object.id)

    return render(
        request,
        'vocabularies/term_list.html',
        {
            'vocabulary': vocab_object,
            'terms': term_list,
            'domain': settings.VOCAB_DOMAIN,
        },
    )


def all_vocabularies(request):
    vocab_dict = {}
    for vocab in Vocabulary.objects.all():
        term_dict = {}
        for term in Term.objects.filter(vocab_list=vocab.id):
            term_dict[term.name] = term.label
        vocab_dict[vocab.name] = term_dict
    return HttpResponse(str(vocab_dict), content_type='text/plain')


def verbose_vocabularies(request):
    vocab_dict = {}
    # Get all the vocabularies
    for vocab in Vocabulary.objects.all():
        term_list = []
        # Get the terms for the vocabulary
        term_objects = Term.objects.filter(vocab_list=vocab.id)
        # Attempt to order the terms by the vocabulary order
        try:
            ordered_term_objects = term_objects.order_by(vocab.order)
        except:     # noqa: E722
            ordered_term_objects = term_objects
        # Loop through the terms
        for term in ordered_term_objects:
            # Create the url for the term
            term_url = "%svocabularies/%s/#%s" % \
                (settings.VOCAB_DOMAIN, vocab.name, term.name)
            # Create the term data dictionary
            term_dict = {
                'name': term.name,
                'label': term.label,
                'order': term.order,
                'url': term_url,
                }
            # Add it to the ordered term list
            term_list.append(term_dict)
        # Add the term list to the vocabulary dictionary
        vocab_dict[vocab.name] = term_list
    return HttpResponse(str(vocab_dict), content_type='text/plain')


def vocabulary_file(request, list_name, file_format):
    try:
        vocab = Vocabulary.objects.get(name__exact=list_name)
    except(Vocabulary.DoesNotExist, Vocabulary.MultipleObjectsReturned):
        raise http.Http404
    if string.upper(file_format) == 'XML':
        vocabulary_object = VocabularyHandler.xml_response(vocab)
    elif string.upper(file_format) == 'PY':
        vocabulary_object = VocabularyHandler.py_response(vocab)
    elif string.upper(file_format) == 'JSON':
        vocabulary_object = VocabularyHandler.json_response(vocab)
    elif string.upper(file_format) == 'TKL':
        vocabulary_object = VocabularyHandler.tkl_response(vocab)

    return HttpResponse(vocabulary_object.vocab_file,
                        content_type=vocabulary_object.vocab_mimetype)
