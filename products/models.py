from django.db import models
from django.conf import settings

class Product(models.Model):
    # Ye product kis exporter ka hai (User se link)
    exporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    moq = models.CharField(max_length=50, help_text="Minimum Order Quantity (e.g. 100 kg)")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    
    def __str__(self):
        return self.name