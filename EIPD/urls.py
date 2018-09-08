"""EIPD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from .views import ContactView, download_guide_PILAR_es, download_manual_es
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('secret/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'),name='home'),
    path('accounts/', include('Register.urls')),
    path('PIAs/', include('PIAs.urls')),
    path('contact/', ContactView.as_view(), name='contact'),
    path('guides/', TemplateView.as_view(template_name='guides.html'), name='guides'),
    path('guides/PILAR_es', download_guide_PILAR_es, name='PILAR_es'),
    path('guides/manual_es', download_manual_es, name='manual_es'),
    path('thanks/', TemplateView.as_view(template_name='contact/contact_success.html'), name='thanks'),
]
