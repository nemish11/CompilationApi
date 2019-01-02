from django.db import models
import datetime
# Create your models here.
class Submissions(models.Model):
    username = models.CharField(max_length=50)
    language = models.CharField(max_length=20)
    isRunning = models.CharField(max_length=20,null=True)
    datetime = models.DateTimeField(null=True)

class Files(models.Model):
    submission = models.ForeignKey(Submissions, on_delete=models.CASCADE, related_name='file_submission')
    type = models.CharField(max_length = 20)
    errortype = models.CharField(max_length=100,null=True)
    runtime = models.CharField(max_length=20,null=True)
    memoryused = models.CharField(max_length=20,null=True)
    filepath = models.CharField(max_length = 100)
