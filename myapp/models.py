from django.db import models

# Create your models here.

class StickyNote(models.Model):
    
    nickname = models.CharField(max_length=13)
    nickname_color = models.CharField(max_length=5)
    nickname_font = models.CharField(max_length=20)
    content = models.TextField(max_length=155)
    content_color = models.CharField(max_length=5)
    content_font = models.CharField(max_length=20)
    emoji = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.nickname
    
    
class UserSuggestion(models.Model):

    nickname = models.CharField(max_length=13)
    subject = models.CharField(max_length=50)
    content = models.TextField()
    
    def __str__(self) -> str:
        return self.subject