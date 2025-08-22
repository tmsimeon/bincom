from django.db import models
import os
from django.utils import timezone

class MediaItem(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='media_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

    def get_upload_path(instance, filename):
        # Create a directory structure: media_type/year/month/filename
        date = timezone.now().strftime("%Y/%m")
        return os.path.join(instance.media_type, date, filename)
    
    file = models.FileField(upload_to=get_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    def file_url(self):
        return self.file.url