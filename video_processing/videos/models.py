from django.db import models

class Video(models.Model):
    # name = models.CharField(max_length=100, default=None)
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title
    
class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='subtitles')
    start_time = models.TimeField()
    end_time = models.TimeField()
    content = models.TextField()
    language = models.CharField(max_length=50, default=None)