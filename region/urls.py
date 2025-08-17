from django.urls import path
from . import views

app_name = 'region'

urlpatterns = [
    path('region/', views.region_page, name='region_default'),
    path('region/<slug:slug>/', views.region_page, name='region_tab'),
    path('region_detail/<slug:slug>/',
         views.listsection_detail, name='region_detail'),
]
