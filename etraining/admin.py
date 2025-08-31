from django.contrib import admin
from .models import ETrainingDocs, ETrainingVideo, ECategory
# Register your models here.
admin.site.register(ETrainingDocs)
admin.site.register(ETrainingVideo)
admin.site.register(ECategory)