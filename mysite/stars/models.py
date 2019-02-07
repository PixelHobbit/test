from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Star(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(default='default.png',upload_to='Images/')
    date = models.DateField()
    text = RichTextUploadingField()

    def __str__(self):
        return "<star: %s>" % self.title
