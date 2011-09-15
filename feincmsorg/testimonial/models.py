from django.db import models


class Testimonial(models.Model):
    is_active = models.BooleanField()
    name = models.CharField(max_length=100)
    text = models.TextField()
