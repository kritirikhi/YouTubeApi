from django.db import models

# Video Modal For Storing Data In Database
class Video(models.Model):
    videoid = models.AutoField(primary_key=True)
    title = models.TextField()
    description = models.TextField()
    thumbnail_url = models.TextField()
    publishedAt = models.DateTimeField()
