from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.http import JsonResponse, HttpResponse
from groq import Groq
from django.conf import settings
from django.contrib import messages # <-- Ye naya import add kiya hai
import json
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime

@login_required(login_url='login')
def add_product_view(request):
    if request.method == 'POST':
        # --- FREE PLAN LIMIT CHECK ---
        if request.user.effective_plan == 'free':
            product_count = Product.objects.filter(exporter=request.user).count()
            if product_count >= 5:
                messages.error(request, "Free plan is limited to 5 products. Please upgrade to Pro for unlimited access.")
                return redirect('dashboard')
        # -----------------------------

        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        moq = request.POST.get('moq')
        
        # Naya product database me save karo, aur usko current user se link karo
        Product.objects.create(
            exporter=request.user,
            name=name,
            description=description,
            price=price,
            moq=moq,
            image=request.FILES.get('image')
        )
        return redirect('dashboard') # Save hone ke baad wapas dashboard pe jao
        
    return render(request, 'add_product.html')


@login_required(login_url='login')
def generate_description_view(request):
    if request.method == 'POST':
        try:
            # JavaScript se product ka naam lena
            data = json.loads(request.body)
            product_name = data.get('product_name', '')
            
            if not product_name:
                return JsonResponse({'error': 'Product name is required'}, status=400)

            # Groq AI ko initialize karna settings.py wali key se
            client = Groq(api_key=settings.GROQ_API_KEY)
            
            # AI ko prompt (command) dena
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional B2B export copywriter. Write a short, attractive, and professional product description for an export website in English. Keep it under 3 sentences. Do not add any extra conversational text, just return the description."
                    },
                    {
                        "role": "user",
                        "content": f"Product Name: {product_name}"
                    }
                ],
                model="openai/gpt-oss-20b",  # Ye Groq ka fast free model hai
            )
            
            # AI ka jawab nikalna
            description = chat_completion.choices[0].message.content
            
            return JsonResponse({'description': description})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url='login')
def delete_product_view(request, product_id):
    # Sirf wahi product delete ho jo current user ka ho
    product = get_object_or_404(Product, id=product_id, exporter=request.user)
    product.delete()
    return redirect('dashboard')


@login_required(login_url='login')
def edit_product_view(request, product_id):
    # Wo product dhoondo jo is user ka ho
    product = get_object_or_404(Product, id=product_id, exporter=request.user)
    
    if request.method == 'POST':
        # Naya data save karo
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.moq = request.POST.get('moq')
        
        # Agar nayi image upload hui hai
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            
        product.save()
        return redirect('dashboard')
        
    # Form me dikhane ke liye product bhej do
    context = {
        'product': product
    }
    return render(request, 'add_product.html', context)


@login_required(login_url='login')
def generate_quotation_pdf(request, product_id):
    # Product dhoondo jo is user ka ho
    product = get_object_or_404(Product, id=product_id, exporter=request.user)
    exporter = request.user

    # Memory me ek khali PDF file (Buffer) banao
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # --- PDF Ka Design (Drawing) ---
    # 1. Header (Company Name)
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, 750, f"{exporter.company_name or exporter.username}")
    
    p.setFont("Helvetica", 10)
    p.drawString(50, 735, f"Email: {exporter.email}")
    p.drawString(50, 720, f"IEC Code: {exporter.iec_code or 'N/A'}")
    p.drawString(50, 705, "India")

    # 2. Title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, 630, "QUOTATION")
    
    # 3. Date
    p.setFont("Helvetica", 10)
    p.drawString(400, 630, f"Date: {datetime.date.today().strftime('%d-%b-%Y')}")

    # 4. Line
    p.line(50, 620, 550, 620)

    # 5. Product Details
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 580, "Product Details:")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 550, f"Product: {product.name}")
    p.drawString(50, 530, f"Description: {product.description or 'High Quality Export Product'}")
    p.drawString(50, 510, f"Price: USD {product.price}")
    p.drawString(50, 490, f"Minimum Order Quantity (MOQ): {product.moq}")

    # 6. Line & Footer
    p.line(50, 450, 550, 450)
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 430, "Thank you for your interest. Please contact us for further details.")

    # PDF save karo
    p.showPage()
    p.save()

    # File pointer ko shuru me le aao
    buffer.seek(0)

    # PDF ko browser me return karo (download ke liye)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Quotation_{product.name}.pdf"'
    return response