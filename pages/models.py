from django.db import models


# Create your models here.
class Image(models.Model):
    file = models.FileField(upload_to="pages")
    uploaded = models.DateTimeField(auto_now_add=True)
    table_data = models.JSONField(default=dict)


def __str__(self):
    return str(self.pk)
