from django.shortcuts import render
from .models import User, SitePage, PricingPlan

# Create your views here.

def home_view(request):
    # Database se saare pricing plans order ke hisaab se nikaalo
    pricing_plans = PricingPlan.objects.all().order_by('order')
    
    context = {
        'pricing_plans': pricing_plans
    }
    
    return render(request, 'home.html', context)