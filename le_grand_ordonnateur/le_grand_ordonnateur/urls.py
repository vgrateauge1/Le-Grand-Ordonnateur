"""
URL configuration for le_grand_ordonnateur project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path

from plm_app import views

handler404 = views.custom_404
handler500 = views.custom_500
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('product_dashboard')),
    path('product_dashboard', views.products_dashboard, name='product_dashboard'),
    path('product-overview/<int:id>', views.product_overview, name='product_overview'),
]