from django import forms
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

from feincms.admin.editor import ItemEditorForm
from feincms_oembed.contents import OembedContent
from form_designer.models import FormContent


MEDIA_TYPE_CHOICES = (
    ('default', _('default')),
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
    text = forms.CharField(widget=forms.Textarea, required=False, label=_('text'))

    def __init__(self, *args, **kwargs):
        super(ArticleContentAdminForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'item-richtext'})


class ArticleContent(models.Model):
    # Choices for link target
    DEFAULT = 1
    BLANK = 2
    SELF = 3
    PARENT = 4
    TOP = 5
    TARGET_CHOICES = (
        (DEFAULT, 'default'),
        (BLANK, '_blank'),
        (SELF, '_self'),
        (PARENT, '_parent'),
        (TOP, '_top'),
    )

    feincms_item_editor_form = ArticleContentAdminForm

    title = models.CharField(max_length=200, blank=True)
    text = models.TextField(blank=True)
    link = models.URLField(verify_exists=False, blank=True)
    link_text = models.CharField(max_length=50, blank=True)
    link_target = models.IntegerField(choices=TARGET_CHOICES, default=DEFAULT, blank=True)
    mediafile = MediaFileForeignKey(MediaFile, blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = "Article Content"
        
    def render(self, **kwargs):
        return render_to_string("content/article/default.html", {'article': self})


Page.register_extensions('changedate', 'navigation', 'ct_tracker')
Page.create_content_type(RichTextContent, regions=('main', 'sidebar', 'moodboard'), cleanse=True)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=MEDIA_TYPE_CHOICES)
Page.create_content_type(OembedContent, DIMENSION_CHOICES=MEDIA_TYPE_CHOICES, regions=('main',))
Page.create_content_type(FormContent)
#Page.create_content_type(OembedContent)
Page.create_content_type(ArticleContent)
