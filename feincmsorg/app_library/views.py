from django.http import HttpResponse

def app_list(request):
    return HttpResponse('ok')

def app_detail(request):
    return HttpResponse('ok')