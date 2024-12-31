from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'shared/error_404.html', status=404)

def custom_500(request):
    return render(request, 'shared/error_500.html', status=500)

def products_dashboard(request):
    return render(request, 'Product/product_dashboard.html')
def product_overview(request):
    return render(request, 'Product/product_overview.html')


