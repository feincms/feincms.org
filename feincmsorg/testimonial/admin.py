from django.contrib import admin

from feincms.testimonial import models


admin.site.register(models.Testimonial,
    list_display=('name', 'text', 'is_active'),
    )
