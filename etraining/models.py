from django.db import models

# Create your models here.
class ECategory(models.Model):
    title = models.CharField(max_length=400)
    lang_code = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class ETrainingVideo(models.Model):
    title = models.CharField(max_length=400)
    video = models.FileField(upload_to='trainings/video/')
    category = models.ForeignKey(ECategory, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.title
    
class ETrainingDocs(models.Model):
    title = models.CharField(max_length=400)
    file = models.FileField(upload_to='trainings/doc/')
    category = models.ForeignKey(ECategory, on_delete=models.CASCADE, related_name='docs')

    def __str__(self):
        return self.title

    
    