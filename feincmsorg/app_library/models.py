from django.db import models
from django.forms.widgets import Textarea
from feincms.translations import TranslatedObjectMixin, Translation
from django.utils.translation import ugettext_lazy as _
from feincms.content.application import models as app_models

from django.contrib.auth.models import User
from django import forms


LICENCE_CHOICES = (('apache', _('apache')),
                   ('gnu', _('GNU')),
                   ('pd', _('public domain')),
                   ('com', _('commercial')),
                   ('other', _('other')),
)


class AppPromo(models.Model, TranslatedObjectMixin):
    title = models.CharField(_('Title'), max_length=50)
    slug = models.SlugField(_('Slug'), max_length=50, unique=True, db_index=True)
    icon = models.ImageField(_('App icon'), upload_to='app_icons', blank=True, null=True,
            help_text=_('A 64x64 pixel Icon for your app (optional)'))
    project_url = models.URLField(_('Project URL'))
    doc_url = models.URLField(_('Documentation URL'), blank=True)
    licence = models.CharField(_('Licence'), max_length=16, choices=LICENCE_CHOICES,
                                             default=LICENCE_CHOICES[0][0])
    author = models.ForeignKey(User)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    download_count = models.IntegerField(_('download count'), default=0)

    class Meta:
        verbose_name = _('App promo')
        verbose_name_plural = _('App promos')
        ordering = ['-updated']

    def __unicode__(self):
        return unicode(self.title)

    @app_models.permalink
    def get_absolute_url(self):
        return ('app_library_detail', 'app_library.urls', (), {'slug': self.slug})


class AppPromoTranslation(Translation(AppPromo)):
    short_description = models.TextField()
    long_description = models.TextField()

    class Meta:
        verbose_name = _('App promo translation')


class AppPromoForm(forms.ModelForm):
    short_description = forms.CharField(max_length=200,
                         widget=Textarea(attrs={'cols': 80, 'rows': 4, 'class': 'richtext' }))
    long_description = forms.CharField(
                        widget=Textarea(attrs={'cols': 80, 'rows': 10, 'class': 'richtext' }))

    class Meta:
        model = AppPromo
        exclude = ('slug', 'author', 'created', 'updated', 'download_count')
