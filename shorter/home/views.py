from django.shortcuts import render, redirect
from django.views import View
from utils.rate_limiter import rate_limit

from .forms import HomeForm
from .models import Url
# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = HomeForm()
        context = {'form':form}
        return render(request, 'home/home.html', context)

    @rate_limit(HomeForm)
    def post(self, request, *args, **kwargs):
        form = HomeForm(request.POST)
        slug = request.POST.get('slug')
        path = request.build_absolute_uri()
        error, slug = Url.validate(self, form, slug, path)
        if not error:
            return render(request, 'home/home.html', 
                {'form':form, 'slug': slug})
        return render(request, 'home/home.html',
            {'form': form, 'error': error})

class RedirectView(View):
    def get(self, request, *args, **kwargs):
        web_url = request.get_full_path()[1:]
        new_url = Url.objects.filter(slug=web_url.lower())
        if len(new_url) > 0:
            return redirect(str(new_url[0]))
        return redirect('/')