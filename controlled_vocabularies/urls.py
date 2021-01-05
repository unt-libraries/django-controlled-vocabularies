from django.urls import path, re_path
from controlled_vocabularies.views import (
    vocabulary_list, verbose_vocabularies, about,
    all_vocabularies, term_list, vocabulary_file
)

urlpatterns = [
    # Search View
    path('', vocabulary_list, name="vocabulary_list"),
    path('all-verbose/', verbose_vocabularies, name="verbose_vocabularies"),
    re_path(r'^all-verbose\.(?P<file_format>py|json)/?$', verbose_vocabularies,
            name="verbose_vocabularies"),
    path('about/', about, name="about"),
    path('all/', all_vocabularies, name="all_vocabularies"),
    re_path(r'^all\.(?P<file_format>py|json)/?$', all_vocabularies, name="all_vocabularies"),
    path('<slug:list_name>/<slug:file_format>/', vocabulary_file,
         name="vocabulary_file"),
    path('<slug:vocabulary_name>/', term_list, name="term_list"),
]
