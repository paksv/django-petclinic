from django.shortcuts import render

def home(request):
    """View function for home page of site."""
    return render(request, 'home.html')

def handler404(request, exception):
    """Custom 404 page not found handler"""
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    """Custom 500 server error handler"""
    return render(request, 'errors/500.html', status=500)

def handler403(request, exception):
    """Custom 403 permission denied handler"""
    return render(request, 'errors/403.html', status=403)

def trigger_error(request):
    """View to deliberately trigger a 500 error for testing"""
    # Intentionally raise an exception to trigger a 500 error
    division_by_zero = 1 / 0
    return render(request, 'home.html')
