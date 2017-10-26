from django.contrib import admin
from django import forms
from controlled_vocabularies.models import Vocabulary, Term, Property


class PropertyInline(admin.TabularInline):
    model = Property
    fk_name = "term_key"
    extra = 1


class VocabularyAdmin(admin.ModelAdmin):
    """ Vocabulary class that determines how comment appears in admin """
    list_display = ('name', 'label', 'order', 'maintainer', 'created', 'modified')
    fieldsets = (
        (None, {
            'classes': 'wide extrapretty',
            'fields': ('name', 'label', 'order', 'maintainer', 'maintainerEmail', 'definition')
        }),
    )


class TermAdmin(admin.ModelAdmin):
    """ Term class that determines how comment appears in admin """
    list_display = ('id', 'name', 'get_vocab', 'label', 'order',)
    fieldsets = (
        (None, {
            'classes': 'wide extrapretty',
            'fields': ('vocab_list', 'name', 'label', 'order')
        }),
    )
    list_filter = ('vocab_list',)
    inlines = [PropertyInline]


class PropertyAdmin(admin.ModelAdmin):
    """ Property class that determines how comment appears in admin """
    list_display = ('property_name', 'get_vocab', 'get_term', 'label',)
    fieldsets = (
        (None, {
            'classes': 'wide extrapretty',
            'fields': ('term_key', 'property_name', 'label')
        }),
    )


def has_spaces(name):
    """ Make sure there are no spaces """
    if ' ' in name:
        raise forms.ValidationError("Spaces are not allowed.")
    else:
        return name


class VocabularyAdminForm(forms.ModelForm):
    """ Vocabulary class to specify how form data is handled in admin """
    class Meta:
        model = Vocabulary
        fields = '__all__'

    def clean_name(self):
        """ Make sure there are no spaces in the name field """
        return has_spaces(self.cleaned_data["name"])


admin.site.register(Vocabulary, VocabularyAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(Property, PropertyAdmin)
