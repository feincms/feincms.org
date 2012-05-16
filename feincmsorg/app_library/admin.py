from django.contrib import admin
from feincms.translations import admin_translationinline, short_language_code
from .models import AppPromo, AppPromoTranslation, Category, CategoryTranslation
from django.utils.translation import ugettext_lazy as _


#TODO: Add richtext class to long_description and TinyMCE to form.

class AppPromoAdmin(admin.ModelAdmin):
    list_display = ('title', 'download_count')
    prepopulated_fields = { "slug": ("title",)}
    inlines = [admin_translationinline(AppPromoTranslation)]

admin.site.register(AppPromo, AppPromoAdmin)

CategoryTranslationInline = admin_translationinline(CategoryTranslation, prepopulated_fields={
    'slug': ('title',)})

class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryTranslationInline]
    list_display = ['__unicode__', 'entries']
    search_fields = ['translations__title']

    def entries(self, obj):
        if 'translations' in getattr(AppPromo, '_feincms_extensions', ()):
            return AppPromo.objects.filter(categories=obj, language=short_language_code()).count()
        return AppPromo.objects.filter(categories=obj)
    entries.short_description = _('Apps in category')

admin.site.register(Category, CategoryAdmin)