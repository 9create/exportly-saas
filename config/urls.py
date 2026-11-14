"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import home_view, blog_list_view,blog_detail_view
from users.views import signup_view,login_view, dashboard_view, logout_view
from django.conf import settings
from django.conf.urls.static import static
from users.views import update_profile_view, public_site_view, add_page_view, custom_page_view, change_theme_view, catalog_view, edit_page_view, delete_page_view,upgrade_plan_view, privacy_policy_view, terms_conditions_view, disclaimer_view, sitemap_view, robots_txt_view, apply_promo_code_view, generate_website_view
from inquiries.views import submit_inquiry_view, inquiry_list_view, mark_inquiry_read_view
from products.views import add_product_view, generate_description_view, delete_product_view, edit_product_view, generate_quotation_pdf
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('blog/', blog_list_view, name='blog_list'),
    path('blog/<slug:slug>/', blog_detail_view, name='blog_detail'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('platform/privacy/', auth_views.TemplateView.as_view(template_name='platform_privacy.html'), name='platform_privacy'),
    path('platform/terms/', auth_views.TemplateView.as_view(template_name='platform_terms.html'), name='platform_terms'),
    path('platform/disclaimer/', auth_views.TemplateView.as_view(template_name='platform_disclaimer.html'), name='platform_disclaimer'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),    
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'), 
    path('dashboard/add-product/', add_product_view, name='add_product'),
    path('dashboard/profile/', update_profile_view, name='update_profile'),
    path('dashboard/generate-website/', generate_website_view, name='generate_website'),
    path('dashboard/upgrade/', upgrade_plan_view, name='upgrade_plan'),
    path('dashboard/apply-promo/', apply_promo_code_view, name='apply_promo'),
    path('site/<str:username>/', public_site_view, name='public_site'),
    path('site/<str:username>/catalog/', catalog_view, name='catalog'),
    path('site/<str:username>/privacy/', privacy_policy_view, name='privacy_policy'),
    path('site/<str:username>/sitemap.xml', sitemap_view, name='sitemap'),
    path('site/<str:username>/robots.txt', robots_txt_view, name='robots_txt'),
    path('site/<str:username>/terms/', terms_conditions_view, name='terms_conditions'),
    path('site/<str:username>/disclaimer/', disclaimer_view, name='disclaimer'),    
    path('dashboard/add-page/', add_page_view, name='add_page'),
    path('dashboard/edit-page/<int:page_id>/', edit_page_view, name='edit_page'),
    path('dashboard/delete-page/<int:page_id>/', delete_page_view, name='delete_page'),    
    path('dashboard/change-theme/<str:theme_name>/', change_theme_view, name='change_theme'),
    path('site/<str:username>/inquiry/', submit_inquiry_view, name='submit_inquiry'),
    path('site/<str:username>/<str:slug>/', custom_page_view, name='custom_page'),
    path('dashboard/inquiries/', inquiry_list_view, name='inquiry_list'),
    path('dashboard/inquiries/mark-read/<int:inquiry_id>/', mark_inquiry_read_view, name='mark_inquiry_read'),    
    path('api/generate-description/', generate_description_view, name='generate_description'),
    path('dashboard/delete-product/<int:product_id>/', delete_product_view, name='delete_product'),   
    path('dashboard/edit-product/<int:product_id>/', edit_product_view, name='edit_product'),
    path('dashboard/generate-quotation/<int:product_id>/', generate_quotation_pdf, name='generate_quotation'),
    prefix_default_language=False
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)