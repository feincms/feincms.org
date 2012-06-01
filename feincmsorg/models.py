from django import forms
from django.contrib import admin
from django.db import models
from django.template.defaultfilters import capfirst
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from feincms.module.medialibrary.models import MediaFile
from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.module.page.models import Page
from feincms.content.application.models import ApplicationContent
from feincms.content.medialibrary.v2 import MediaFileContent
from feincms.content.richtext.models import RichTextContent

from feincms.admin.item_editor import FeinCMSInline, ItemEditorForm
from feincms_oembed.contents import OembedContent
from form_designer.models import FormContent

from elephantblog.models import Entry


MEDIA_TYPE_CHOICES = (
    ('default', _('default')),
)

DIMENSION_CHOICES = (
    ('590x432', _('default')),
)

Page.register_templates({
    'title': 'Standard template',
    'path': 'page_default.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ('moodboard', _('Moodboard'), 'inherited'),
        ),
    },{
    'title': 'Homepage template',
    'path': 'page_home.html',
    'regions': (
        ('main', _('Main content area')),
        ('moodboard', _('Moodboard'), 'inherited'),
        ),
    })


class ArticleContentAdminForm(ItemEditorForm):
    def __init__(self, *args, **kwargs):
        super(ArticleContentAdminForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'item-richtext'})


class ArticleContentInline(FeinCMSInline):
    form = ArticleContentAdminForm
    raw_id_fields = ('mediafile',)


class ArticleContent(models.Model):
    feincms_item_editor_inline = ArticleContentInline

    title = models.CharField(_('title'), max_length=200, blank=True)
    text = models.TextField(_('text'), blank=True)
    link = models.URLField(verify_exists=False, blank=True)
    link_text = models.CharField(max_length=50, blank=True)
    mediafile = MediaFileForeignKey(MediaFile, blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = "Article content"

    def render(self, **kwargs):
        return render_to_string([
            "content/article/%s.html" % self.region,
            "content/article/default.html",
            ], {'content': self})


Page.register_extensions('changedate', 'navigation', 'ct_tracker')
Page.create_content_type(RichTextContent, regions=('main', 'sidebar', 'moodboard'), cleanse=True)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=MEDIA_TYPE_CHOICES)
Page.create_content_type(OembedContent, DIMENSION_CHOICES=DIMENSION_CHOICES, regions=('main',))
Page.create_content_type(FormContent)
Page.create_content_type(ArticleContent)

Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('feincmsorg.app_library.urls', 'App Library'),
    ))

Entry.register_regions(
    ('main', _('Main content area')),
    )
Entry.create_content_type(RichTextContent, cleanse=True)
Entry.create_content_type(MediaFileContent, TYPE_CHOICES=MEDIA_TYPE_CHOICES)
Entry.create_content_type(OembedContent, DIMENSION_CHOICES=DIMENSION_CHOICES, regions=('main',))
