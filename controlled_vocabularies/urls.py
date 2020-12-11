from django.urls import re_path
from controlled_vocabularies.views import (
    vocabulary_list, verbose_vocabularies, about,
    all_vocabularies, term_list, vocabulary_file
)

urlpatterns = [
    # Search View
    re_path(r'^$', vocabulary_list, name="vocabulary_list"),
    re_path(r'^all-verbose/?$', verbose_vocabularies, name="verbose_vocabularies"),
    re_path(r'^all-verbose\.(?P<file_format>py|json)/?$', verbose_vocabularies,
            name="verbose_vocabularies"),
    re_path(r'^about/', about, name="about"),
    re_path(r'^all/?$', all_vocabularies, name="all_vocabularies"),
    re_path(r'^all\.(?P<file_format>py|json)/?$', all_vocabularies, name="all_vocabularies"),
    re_path(r'^(?P<vocabulary_name>[\w-]+)/$', term_list, name="term_list"),
    re_path(r'^(?P<list_name>[\w-]+)/(?P<file_format>\w+)/$', vocabulary_file,
            name="vocabulary_file"),
]
