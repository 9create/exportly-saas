from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    is_exporter = models.BooleanField(default=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    iec_code = models.CharField(max_length=10, blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    template_choice = models.CharField(max_length=50, default='classic')
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    current_plan = models.CharField(max_length=20, default='free') 
    trial_ends_at = models.DateTimeField(blank=True, null=True)
    brand_color = models.CharField(max_length=7, default="#3758F9")

    @property
    def is_trial_active(self):
        if self.current_plan == 'pro' and self.trial_ends_at:
            return timezone.now() < self.trial_ends_at
        return False

    @property
    def effective_plan(self):
        # Agar user Pro hai, par uska trial date set hai aur wo expire ho chuka hai
        if self.current_plan == 'pro' and self.trial_ends_at and not self.is_trial_active:
            return 'free' 
        # Warna jo current plan hai wahi dikhao (Paid Pro ya Enterprise)
        return self.current_plan

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
    
class PricingPlan(models.Model):
    name = models.CharField(max_length=50) # e.g. Pro Exporter
    description = models.CharField(max_length=200, blank=True, null=True)
    
    # Monthly aur Yearly Prices INR me
    price_monthly_inr = models.DecimalField(max_digits=10, decimal_places=2)
    price_yearly_inr = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Features ek comma-separated string me
    features = models.TextField(help_text="Comma separated features")
    
    # Button ka text (e.g. "Start Free Trial" ya "Contact Sales")
    button_text = models.CharField(max_length=50, default="Get Started")
    
    # Kya ye plan "Most Popular" highlight hoga?
    is_popular = models.BooleanField(default=False)
    
    # Order (taaki website par left to right kis order me dikhe)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name
        
    # Ye naya code add karo (features ko alag karne ke liye):
    @property
    def features_list(self):
        if self.features:
            return [f.strip() for f in self.features.split(',')]
        return []

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="Enter code like EXPORTLY100")
    is_active = models.BooleanField(default=True)
    valid_until = models.DateTimeField(blank=True, null=True, help_text="Leave blank for never expire")

    def __str__(self):
        return self.code  

    
class PlatformSettings(models.Model):
    primary_color = models.CharField(max_length=7, default="#2563EB", help_text="Hex code e.g. #2563EB")
    secondary_color = models.CharField(max_length=7, default="#10B981", help_text="Hex code e.g. #10B981")

    def save(self, *args, **kwargs):
        # Sirf ek hi settings record banega (Singleton)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Platform Settings"      