from django.urls import path, include
from .views import login_view,logout_view,register_view, logout_url_view,profile_view

urlpatterns = [
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('logout_url_view', logout_url_view, name='logout_url_view'),
    path('register', register_view, name='register'),
    path('profile', profile_view, name='profile_view'),
]
