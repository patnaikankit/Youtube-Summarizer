from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SavedSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yt_title = models.CharField(max_length=200)
    yt_link = models.URLField()
    generated_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.yt_title
