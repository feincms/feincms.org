from django.contrib import admin
from feincms.translations import admin_translationinline
from .models import AppPromo, AppPromoTranslation


#TODO: Add richtext class to long_description and TinyMCE to form.

class AppPromoAdmin(admin.ModelAdmin):
    list_display = ('title', 'download_count')
    prepopulated_fields = { "slug": ("title",)}
    inlines = [admin_translationinline(AppPromoTranslation)]

admin.site.register(AppPromo, AppPromoAdmin)