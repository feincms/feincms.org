from django.db import models
from feincms.translations import TranslatedObjectMixin, Translation
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User


LICENCE_CHOICES = (('apache', _('apache')),
                   ('gnu', _('GNU')),
                   ('pd', _('public domain')),
                   ('com', _('commercial')),
                   ('other', _('other')),
)


class AppPromo(models.Model, TranslatedObjectMixin):
    title = models.CharField(_('Title'), max_length=100)
    icon = models.ImageField(_('App icon'), upload_to='app_icons', blank=True, null=True,
            help_text=_('A 64x64 pixel Icon for your app (optional)'))
    project_url = models.URLField(_('Project URL'))
    doc_url = models.URLField(_('Documentation URL'), blank=True)
    licence = models.CharField(_('Licence'), max_length=16, choices=LICENCE_CHOICES,
                                             default=LICENCE_CHOICES[0][0])
    author = models.ForeignKey(User)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        verbose_name = _('App promo')
        verbose_name_plural = _('App promos')
        ordering = ['-updated']

    def __unicode__(self):
        return unicode(self.title)


class AppPromoTranslation(Translation(AppPromo)):
    short_description = models.TextField()
    long_description = models.TextField()

    class Meta:
        verbose_name = _('App promo translation')