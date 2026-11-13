from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User, SitePage, PromoCode  # <--- Yahan SitePage add kiya hai
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        company_name = request.POST.get('company_name')
        
        # Naya user banate waqt Trial set karo
        user = User.objects.create_user(
            username=username, 
            email=email,
            password=password,
            company_name=company_name,
            current_plan='pro', # Trial ke liye pro set kiya
            trial_ends_at=timezone.now() + timedelta(days=15) # Ab 15 din ka trial hoga
        )
        return redirect('home')
        
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard_view(request):
    my_products = Product.objects.filter(exporter=request.user)
    my_pages = SitePage.objects.filter(exporter=request.user)

    context = {
        'products': my_products,
        'pages': my_pages,
    }
    return render(request, 'dashboard.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def update_profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.company_name = request.POST.get('company_name')
        user.phone = request.POST.get('phone')
        user.whatsapp_number = request.POST.get('whatsapp_number')
        user.youtube_link = request.POST.get('youtube_link')
        user.linkedin_link = request.POST.get('linkedin_link')
        user.instagram_link = request.POST.get('instagram_link')
        user.facebook_link = request.POST.get('facebook_link')
        
        # NAYA: Custom Legal Pages Save karna
        user.custom_privacy_policy = request.POST.get('custom_privacy_policy')
        user.custom_terms_conditions = request.POST.get('custom_terms_conditions')
        user.custom_disclaimer = request.POST.get('custom_disclaimer')
        
        if 'cover_image' in request.FILES:
            user.cover_image = request.FILES['cover_image']
            
        color_input = request.POST.get('brand_color')
        if color_input:
            if not color_input.startswith('#'):
                user.brand_color = '#' + color_input
            else:
                user.brand_color = color_input
        user.save()
        return redirect('dashboard')
        
    return render(request, 'update_profile.html')


def public_site_view(request, username):
    exporter = get_object_or_404(User, username=username)
    products = Product.objects.filter(exporter=exporter)
    pages = SitePage.objects.filter(exporter=exporter)

    # Theme Check Logic
    if exporter.template_choice == 'play':
        template_name = 'themes/play/index.html'
    else:
        template_name = 'public_site.html' # Purani themes (classic/modern/minimal)

    context = {
        'exporter': exporter,
        'products': products,
        'pages': pages
    }
    return render(request, template_name, context)


@login_required(login_url='login')
def add_page_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        slug = slugify(title)
        
        SitePage.objects.create(
            exporter=request.user,
            title=title,
            slug=slug,
            content=content
        )
        return redirect('dashboard')
        
    return render(request, 'add_page.html')

def custom_page_view(request, username, slug):
    # Us user ka wo specific page dhoondo
    page = get_object_or_404(SitePage, exporter__username=username, slug=slug)
    pages = SitePage.objects.filter(exporter=page.exporter)
    
    # Theme Check Logic
    if page.exporter.template_choice == 'play':
        template_name = 'themes/play/custom_page.html'
    else:
        template_name = 'custom_page.html'
    
    context = {
        'page': page,
        'exporter': page.exporter,
        'pages': pages
    }
    return render(request, template_name, context)


@login_required(login_url='login')
def change_theme_view(request, theme_name):
    # Current user ki theme update karo
    user = request.user
    user.template_choice = theme_name
    user.save()
    return redirect('dashboard')

def catalog_view(request, username):
    exporter = get_object_or_404(User, username=username)
    products = Product.objects.filter(exporter=exporter)
    pages = SitePage.objects.filter(exporter=exporter)
    
    # Theme Check Logic
    if exporter.template_choice == 'play':
        template_name = 'themes/play/catalog.html'
    else:
        template_name = 'catalog.html'

    context = {
        'exporter': exporter,
        'products': products,
        'pages': pages
    }
    return render(request, template_name, context)

@login_required(login_url='login')
def edit_page_view(request, page_id):
    # Current user ka page dhoondo
    page = get_object_or_404(SitePage, id=page_id, exporter=request.user)
    
    if request.method == 'POST':
        page.title = request.POST.get('title')
        page.content = request.POST.get('content')
        page.slug = slugify(page.title) # Title badalne par URL slug bhi update ho jaye
        page.save()
        return redirect('dashboard')
        
    context = {
        'page': page
    }
    return render(request, 'edit_page.html', context)

@login_required(login_url='login')
def delete_page_view(request, page_id):
    # Sirf apna hi page delete kar sake
    page = get_object_or_404(SitePage, id=page_id, exporter=request.user)
    page.delete()
    return redirect('dashboard')

def privacy_policy_view(request, username):
    exporter = get_object_or_404(User, username=username)
    return render(request, 'privacy_policy.html', {'exporter': exporter})

def terms_conditions_view(request, username):
    exporter = get_object_or_404(User, username=username)
    return render(request, 'terms_conditions.html', {'exporter': exporter})

def disclaimer_view(request, username):
    exporter = get_object_or_404(User, username=username)
    return render(request, 'disclaimer.html', {'exporter': exporter})

@login_required(login_url='login')
def upgrade_plan_view(request):
    return render(request, 'upgrade.html')

def sitemap_view(request, username):
    exporter = get_object_or_404(User, username=username)
    products = Product.objects.filter(exporter=exporter)
    pages = SitePage.objects.filter(exporter=exporter)
    
    # Base URL (Localhost for now, VPS par domain ka naam hoga)
    base_url = f"http://{request.get_host()}/site/{exporter.username}"
    
    # XML Content banayein
    xml_content = f'<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # 1. Homepage
    xml_content += f'  <url>\n    <loc>{base_url}/</loc>\n    <priority>1.0</priority>\n  </url>\n'
    
    # 2. Catalog Page
    xml_content += f'  <url>\n    <loc>{base_url}/catalog/</loc>\n    <priority>0.8</priority>\n  </url>\n'
    
    # 3. Custom Pages
    for page in pages:
        xml_content += f'  <url>\n    <loc>{base_url}/{page.slug}/</loc>\n    <priority>0.6</priority>\n  </url>\n'
        
    xml_content += '</urlset>'
    
    return HttpResponse(xml_content, content_type="application/xml")

def robots_txt_view(request, username):
    # Base URL nikaalo
    base_url = f"http://{request.get_host()}/site/{username}"
    
    content = f"User-agent: *\n"
    content += f"Allow: /\n"
    content += f"Disallow: /dashboard/\n" # Dashboard ko search me mat dikhao
    content += f"Disallow: /admin/\n"     # Admin ko search me mat dikhao
    content += f"\nSitemap: {base_url}/sitemap.xml\n"
    
    return HttpResponse(content, content_type="text/plain")


@login_required(login_url='login')
def apply_promo_code_view(request):
    if request.method == 'POST':
        code_entered = request.POST.get('promo_code')
        try:
            # Check karo code valid aur active hai ya nahi
            promo = PromoCode.objects.get(code=code_entered, is_active=True)
            
            # Expiry check
            if promo.valid_until and timezone.now() > promo.valid_until:
                messages.error(request, 'This promo code has expired.')
            else:
                # Upgrade user to Pro
                user = request.user
                user.current_plan = 'pro'
                user.trial_ends_at = None # Trial khatam, ab permanent pro
                user.save()
                messages.success(request, 'Promo code applied successfully! You are now on the Pro plan.')
                
        except PromoCode.DoesNotExist:
            messages.error(request, 'Invalid or inactive promo code.')
            
    return redirect('upgrade_plan')


@login_required(login_url='login')
def generate_website_view(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        theme = request.POST.get('theme')

        # User ka data update karo
        user = request.user
        if company_name:
            user.company_name = company_name
        if theme:
            user.template_choice = theme
        user.save()

        # Success message dikhao
        messages.success(request, "🎉 Boom! Your website is ready.")
        
        # User ko seedha uski live website par bhej do taaki woh result dekh sake
        return redirect('public_site', username=user.username)
        
    return redirect('dashboard')