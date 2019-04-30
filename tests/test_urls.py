from django.urls import resolve

from controlled_vocabularies import views


def test_vocabulary_list():
    assert resolve('/vocabularies/').func == views.vocabulary_list


def test_verbose_vocabularies():
    assert resolve('/vocabularies/all-verbose/').func == views.verbose_vocabularies


def test_verbose_vocabularies_json():
    assert resolve('/vocabularies/all-verbose.json').func == views.verbose_vocabularies


def test_about():
    assert resolve('/vocabularies/about/').func == views.about


def test_all_vocabularies():
    assert resolve('/vocabularies/all/').func == views.all_vocabularies


def test_all_vocabularies_json():
    assert resolve('/vocabularies/all.json').func == views.all_vocabularies


def test_term_list():
    assert resolve('/vocabularies/some_vocab_name/').func == views.term_list


def test_vocabulary_file():
    assert resolve('/vocabularies/some_list_name/some_format/').func == views.vocabulary_file
