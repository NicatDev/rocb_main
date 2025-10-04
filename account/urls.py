from django.urls import path, include
from .views import login_view,logout_view,register_view, logout_url_view,profile_view, pending_approvals_view, approve_user, reject_user

urlpatterns = [
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('logout_url_view', logout_url_view, name='logout_url_view'),
    path('register', register_view, name='register'),
    path('profile', profile_view, name='profile_view'),
    path('pending-approvals/', pending_approvals_view, name='pending_approvals'),
    path('approve-user/<int:user_id>/', approve_user, name='approve_user'),
    path('reject-user/<int:user_id>/', reject_user, name='reject_user'),
]
