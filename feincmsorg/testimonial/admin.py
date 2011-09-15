from django.contrib import admin

from feincmsorg.testimonial import models


admin.site.register(models.Testimonial,
    list_display=('name', 'text', 'is_active'),
    )
