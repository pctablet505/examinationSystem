from django.db import models


# Create your models here.
class QuestionPaper(models.Model):
    subject = models.CharField(max_length=30)
    date = models.DateField()
    paper = models.JSONField()
