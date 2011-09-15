from django import template

from feincmsorg.testimonial.models import Testimonial


register = template.Library()


@register.assignment_tag
def get_testimonials():
    return Testimonial.objects.filter(is_active=True).order_by('?')
