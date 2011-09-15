from django.contrib import admin
from django.db import models

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'is_active')


class Testimonial(models.Model):
    is_active = models.BooleanField()
    name = models.CharField(max_length=100)
    text = models.TextField()

admin.site.register(Testimonial, TestimonialAdmin)
