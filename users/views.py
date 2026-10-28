from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User, SitePage  # <--- Yahan SitePage add kiya hai
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.utils.text import slugify


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        company_name = request.POST.get('company_name')
        
        user = User.objects.create_user(
            username=username, 
            email=email,
            password=password,
            company_name=company_name
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
        
        if 'cover_image' in request.FILES:
            user.cover_image = request.FILES['cover_image']
            
        user.save()
        return redirect('dashboard')
        
    return render(request, 'update_profile.html')


def public_site_view(request, username):
    exporter = get_object_or_404(User, username=username)
    products = Product.objects.filter(exporter=exporter)
    pages = SitePage.objects.filter(exporter=exporter)

    context = {
        'exporter': exporter,
        'products': products,
        'pages': pages
    }
    return render(request, 'public_site.html', context)


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
    
    context = {
        'page': page,
        'exporter': page.exporter
    }
    return render(request, 'custom_page.html', context)