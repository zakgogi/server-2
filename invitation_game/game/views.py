from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

# Create your views here.
def home(req, name = 'person'):
        context = {"name": name}
    
        return render(req, "game/index.html", context)
        
def not_found_404(request, exception):
    data = { 'err': exception }
    return render(request, 'game/404.html', data)

def server_error_500(request):
    return render(request, 'game/500.html')
