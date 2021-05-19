from django.db import models
from django.contrib.sites.models import Site
from django.utils.timezone import now
from django.utils.safestring import mark_safe

ORDER_CHOICES = (
        ('name', 'name'),
        ('label', 'label'),
        ('order', 'order'),
    )

PROPERTY_NAME_CHOICES = (
    ('description', 'Description'),
    ('note', 'Note'),
    ('system', 'System'),
)


class Vocabulary(models.Model):
    """ Vocabulary Model """
    name = models.CharField(
        max_length=50,
        help_text="The name or key that uniquely identifies the vocabulary.",
        unique=True,
        )
    label = models.CharField(
        max_length=255,
        help_text="The human-readable name of the vocabulary.",
        )
    order = models.CharField(
        max_length=10,
        choices=ORDER_CHOICES,
        help_text="The preferred order for viewing the UNTL list of controlled vocabularies.",
        )
    maintainer = models.CharField(
        max_length=50,
        help_text="The person responsible for creating and updating the vocabulary.",
        )
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(
        editable=False,
        auto_now=True,
        )
    maintainerEmail = models.CharField(
        "Maintainer E-mail",
        max_length=50,
        help_text="E-mail address of maintainer.",
        )
    definition = models.TextField(
        blank=True,
        help_text="A brief statement of the meaning of the vocabulary.",
        )

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = now()
        self.name = self.name.strip()
        self.label = self.label.strip()
        super(Vocabulary, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Vocabularies"
        ordering = ['name']


class Term(models.Model):
    """ Term Model """
    vocab_list = models.ForeignKey(
        Vocabulary,
        on_delete=models.CASCADE,
        verbose_name="Vocabulary",
        help_text="The vocabulary that the term needs to be added to.",
        )
    name = models.CharField(
        max_length=50,
        help_text="The name or key that uniquely identifies the term within the vocabulary.",
        )
    label = models.CharField(
        max_length=255,
        help_text="The human-readable name of the term.",
        )
    order = models.IntegerField(
        blank=True,
        null=True,
        help_text="The preferred order for viewing the term in the vocabulary.",
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.vocab_list.modified = now()
        self.name = self.name.strip()
        self.label = self.label.strip()
        super(Term, self).save(*args, **kwargs)
        self.vocab_list.save()

    def get_vocab(self):
        return mark_safe("<a href=\'http://%s/admin/controlled_vocabularies/vocabulary/%s\'>%s</a>" %
                         (Site.objects.get_current().domain, self.vocab_list.id, self.vocab_list))
    get_vocab.short_description = 'Vocabulary'
    get_vocab.allow_tags = True

    class Meta:
        verbose_name_plural = "Terms"
        unique_together = ("name", "vocab_list")
        ordering = ['name']


class Property(models.Model):
    """ Property Model """
    term_key = models.ForeignKey(
        Term,
        on_delete=models.CASCADE,
        verbose_name="Term",
        )
    property_name = models.CharField(
        "Property Type",
        choices=PROPERTY_NAME_CHOICES,
        max_length=50,
        help_text="The name of the added property; e.g., 'Description'.",
        )
    label = models.TextField(
        help_text="The value for the added property.",
        )

    def save(self, *args, **kwargs):
        self.property_name = self.property_name.lower()
        self.term_key.vocab_list.modified = now()
        self.label = self.label.strip()
        super(Property, self).save(*args, **kwargs)
        self.term_key.vocab_list.save()

    def get_vocab(self):
        return mark_safe("<a href=\'http://%s/admin/controlled_vocabularies/vocabulary/%s\'>%s</a>" %
                         (Site.objects.get_current().domain,
                          self.term_key.vocab_list.id, self.term_key.vocab_list))
    get_vocab.short_description = 'Vocabulary'
    get_vocab.allow_tags = True

    def get_term(self):
        return mark_safe("<a href=\'http://%s/admin/controlled_vocabularies/term/%s\'>%s</a>" %
                         (Site.objects.get_current().domain, self.term_key.id, self.term_key))
    get_term.short_description = 'Term'
    get_term.allow_tags = True

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['property_name']
