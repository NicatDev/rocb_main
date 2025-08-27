from django.urls import path
from . import views


urlpatterns = [
    path('newsletters/', views.newsletter_page, name='newsletters'),
    path('outreach-materials/', views.outreach_page, name='outreach'),
    path('gallery/', views.gallery_page, name='gallery'),
    path('cct-centers/', views.cct_center_page, name='cct_centers'),
    path('utilize-our-premises/', views.utilize_our_premises_page,
         name='utilize_our_premises'),
    path('surveys/', views.survey_page, name='survey'),
    path('survey/<int:survey_id>/view/',
         views.survey_pdf_view, name='survey_pdf_view'),
]
