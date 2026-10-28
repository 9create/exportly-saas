from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_exporter = models.BooleanField(default=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    iec_code = models.CharField(max_length=10, blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    
    def __str__(self):
        return self.username

class SitePage(models.Model):
    exporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200) # URL ke liye (e.g. about-us)
    content = models.TextField(blank=True) # Abhi ke liye text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.exporter.username} - {self.title}"    