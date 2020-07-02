from django.core.cache import cache
from django.shortcuts import render

def rate_limit(return_form,limit=30):
    def f_decorator(func):
        def f_wrapper(self, request, *args, **kwargs):
            ip = request.META.get('REMOTE_ADDR')
            value = cache.get(ip) or 0
            if not value or value < 2:
                value += 1
                cache.set(ip, value, limit)
                return func(self, request,*args, **kwargs)
            form = return_form(request.POST)
            context = {
            'form': form, 
            'error': f'You have to wait {limit} seconds!'}
            return render(request, 'home/home.html', context)
        return f_wrapper
    return f_decorator