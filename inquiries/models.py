from django.db import models
from django.conf import settings
from products.models import Product

class Inquiry(models.Model):
    # Ye message kis exporter (user) ke liye aaya hai
    exporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inquiries')
    
    # Buyer kis product ke liye message kar raha hai (optional)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Buyer ki details
    buyer_name = models.CharField(max_length=100)
    buyer_email = models.EmailField()
    buyer_country = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False) # Naya field: Padha gaya ya nahi
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer_name} - {self.exporter.username}"