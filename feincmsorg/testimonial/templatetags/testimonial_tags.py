from django import template

from feincmsorg.testimonial.models import Testimonial

register = template.Library()

def do_load_testimonials(parser, token):
    return TestimonialsNode()


class TestimonialsNode(template.Node):
    def render(self, context):
        context['testimonials'] = Testimonial.objects.filter(is_active = True).order_by('?')
        return ''

register.tag("load_testimonials", do_load_testimonials)
