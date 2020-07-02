from django.urls import path
from django.conf.urls import url

from .views import HomeView, RedirectView

urlpatterns = [
    path('', HomeView.as_view()),
    url(r'', RedirectView.as_view()),
]
