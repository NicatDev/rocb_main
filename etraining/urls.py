from django.urls import path, include
from . import views

app_name = 'training'

urlpatterns = [
    path('', views.language_selection, name='language_selection'),
    
    path('<str:language_code>/', views.content_type_selection, name='content_type_selection'),
    
    path('<str:language_code>/read/', views.read_content_list, name='read_content_list'),
    path('<str:language_code>/read/<slug:slug>/', views.read_content_detail, name='read_content_detail'),
    
    path('<str:language_code>/watch/', views.watch_content_list, name='watch_content_list'),
    path('<str:language_code>/watch/<slug:slug>/', views.watch_content_detail, name='watch_content_detail'),
    
    path('<str:language_code>/webinar/<int:webinar_id>/', views.webinar_detail, name='webinar_detail'),
    
    path('api/<str:language_code>/<str:content_type>/', views.api_content_by_language, name='api_content'),
]
