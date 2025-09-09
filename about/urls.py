from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('about/', views.about_page, name='about_default'),
    path('about/<slug:slug>/', views.about_page, name='about_tab'),
    path('contact-point/', views.contact_point_view, name='contact_point_view'),
]
