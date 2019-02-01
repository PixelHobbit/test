from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod

class ViewType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class View(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    view_type = models.ForeignKey(ViewType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<view: %s>" % self.title

    class Meta:
        ordering = ['-created_time']
