from django.urls import path, include
from .views import set_language, home

urlpatterns = [
    path('set_language/<language>', set_language, name='set_language'),
    path('', home, name='home'),
]
