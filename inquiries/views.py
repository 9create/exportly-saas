from django.shortcuts import render, redirect, get_object_or_404
from .models import Inquiry
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # <-- Ye line file ke sabse upar (imports me) add karo

def submit_inquiry_view(request, username):
    exporter = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        buyer_name = request.POST.get('buyer_name')
        buyer_email = request.POST.get('buyer_email')
        buyer_country = request.POST.get('buyer_country')
        message = request.POST.get('message')
        
        Inquiry.objects.create(
            exporter=exporter,
            buyer_name=buyer_name,
            buyer_email=buyer_email,
            buyer_country=buyer_country,
            message=message
        )
        
        # URL me success=1 daalne ke bajaye Django ka message framework use karo
        messages.success(request, "Your inquiry has been sent successfully. The exporter will contact you soon.")
        
        return redirect('public_site', username=username)
        
    return redirect('public_site', username=username)


@login_required(login_url='login')
def inquiry_list_view(request):
    # Current logged-in user ki saari inquiries nikaalo
    my_inquiries = Inquiry.objects.filter(exporter=request.user).order_by('-created_at')
    
    context = {
        'inquiries': my_inquiries
    }
    return render(request, 'inquiry_list.html', context)