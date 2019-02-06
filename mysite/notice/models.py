from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Notice(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField()
    text = RichTextUploadingField()

    def __str__(self):
       return self.title
