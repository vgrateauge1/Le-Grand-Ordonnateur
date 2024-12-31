from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'error_pages/error_404.html', status=404)

def custom_500(request):
    return render(request, 'error_pages/error_500.html', status=500)

def products_dashboard(request):
    return render(request, 'product/product_dashboard.html')
def product_overview(request):
    return render(request, 'product/product_overview.html')


