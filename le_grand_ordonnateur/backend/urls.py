from backend.views.column_viewset import ColumnViewSet
from backend.views.manufacturing_viewset import ManufacturingViewSet
from backend.views.material_viewset import MaterialViewSet
from backend.views.product_material_viewset import ProductMaterialViewSet
from backend.views.product_version_viewset import ProductVersionViewSet
from backend.views.product_viewset import ProductViewSet
from backend.views.supplier_viewset import SupplierViewSet
from backend.views.task_viewset import TaskViewSet
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from backend.views.product_stock_viewset import ProductStockViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'products/versions', ProductVersionViewSet)
router.register(r'products/materials', ProductMaterialViewSet)
router.register(r'product-stock', ProductStockViewSet, basename='product-stock')
router.register(r'materials', MaterialViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'columns', ColumnViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'manufacturing', ManufacturingViewSet)

def get_csrf_token(request):
    token = get_token(request)
    print(f"CSRF Token: {token}")
    response = JsonResponse({'csrfToken': token})
    response.set_cookie('csrftoken', token)
    return response

# Include the router's URLs
urlpatterns = [
    path('', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('csrf-token/', get_csrf_token, name='csrf_token'),
]