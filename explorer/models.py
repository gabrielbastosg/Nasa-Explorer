from django.db import models

# Create your models here.
class Favorite(models.Model):
    title = models.CharField(max_length=200)
    url= models.URLField()
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

class History(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    apod_date = models.DateField()  #data do APOD
    visited_at = models.DateTimeField(auto_now_add=True) # Quando Visitou
    likes = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.title} ({self.apod_date})"