from django.urls import path, include
from .views import set_language, home, news_page, events_detail, news_detail, events_page, meeting_documents, meeting_documents_single

urlpatterns = [
    path('set_language/<language>', set_language, name='set_language'),
    path('', home, name='home'),
    path('news', news_page, name='news'),
    path('news/<slug>', news_detail, name='news_detail'),
    path('events', events_page, name='events'),
    path('events/<slug>', events_detail, name='events_detail'),
    path('meeting-documents/', meeting_documents, name='meeting_documents'),
    path('meeting-documents/<slug>', meeting_documents_single, name='meeting_documents_single'),
    
]
