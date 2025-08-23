from django.urls import path
from . import views


urlpatterns = [
    path('/newsletters', views.newsletter_page, name='newsletters'),
    path('/outreach-materials', views.outreach_page, name='outreach'),
]
