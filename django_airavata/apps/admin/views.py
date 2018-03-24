from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def app_catalog(request):
    request.active_nav_item = 'app_catalog'
    return render(request, 'admin/app_catalog.html')

@login_required
def credential_store(request):
    request.active_nav_item = 'credential_store'
    return render(request, 'admin/credential_store.html')
