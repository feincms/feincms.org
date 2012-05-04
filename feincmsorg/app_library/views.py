from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from feincmsorg.app_library.models import AppPromo, AppPromoForm, AppPromoTranslation

def app_list(request):
    apps = AppPromo.objects.all()
    context = {'apps': apps }
    return render(request, 'app_library/app_list.html', context)

def app_detail(request, slug):
    app = get_object_or_404(AppPromo, slug=slug)
    return render(request, 'app_library/app_detail.html', {'app': app })

@login_required(login_url='/accounts/login/')
def app_submit(request):
    if request.method == 'POST':
        form = AppPromoForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.slug = slugify(app.title)
            app.author = request.user
            app.save()
            translation = AppPromoTranslation(parent=app, language_code='en')
            translation.short_description = form.cleaned_data['short_description']
            translation.long_description = form.cleaned_data['long_description']
            translation.save()
            return HttpResponseRedirect(app.get_absolute_url())
    else:
        form = AppPromoForm()
    return render(request, 'app_library/submit.html', {'form': AppPromoForm })