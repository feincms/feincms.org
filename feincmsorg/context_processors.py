from feincms.module.page.models import Page


def meta_navigation(request):
    return {
        'meta_navigation': Page.objects.in_navigation().filter(parent___cached_url='/meta/'),
        }
