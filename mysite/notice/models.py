from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField()
    text = models.TextField()

    def __str__(self):
       return self.title
