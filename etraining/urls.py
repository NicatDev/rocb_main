from django.urls import path
from .views import etraining


urlpatterns = [
    path("e-training/docs/", etraining, {"is_video": False}, name="e_training_docs"),
    path("e-training/videos/", etraining, {"is_video": True}, name="e_training_videos"),
]