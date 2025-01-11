from django.urls import path, include
from rest_framework.routers import DefaultRouter

from backend.views import supplier_viewset
from backend.views.material_viewset import MaterialViewSet
from backend.views.product_material_viewset import ProductMaterialViewSet
from backend.views.product_version_viewset import ProductVersionViewSet
from backend.views.product_viewset import ProductViewSet
from backend.views.supplier_viewset import SupplierViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'products/versions', ProductVersionViewSet)
router.register(r'products/materials', ProductMaterialViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'suppliers', SupplierViewSet)

# Include the router's URLs
urlpatterns = [
    path('', include(router.urls)),
]