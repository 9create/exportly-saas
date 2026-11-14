from django.shortcuts import render
from .models import User, SitePage, PricingPlan
from .models import BlogPost
from django.shortcuts import get_object_or_404

# Create your views here.

def home_view(request):
    # Database se saare pricing plans order ke hisaab se nikaalo
    pricing_plans = PricingPlan.objects.all().order_by('order')
    
    context = {
        'pricing_plans': pricing_plans
    }
    
    return render(request, 'home.html', context)


def blog_list_view(request):
    # Sirf wahi posts dikhao jo publish ho chuki hain, latest sabse pehle
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    
    context = {
        'posts': posts
    }
    return render(request, 'blog_list.html', context)


def blog_detail_view(request, slug):
    # Us specific post ko dhoondo jo publish ho chuki ho aur jiska slug match kare
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Baaki posts (Related posts ke liye) - optional
    related_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts
    }
    return render(request, 'blog_detail.html', context)
