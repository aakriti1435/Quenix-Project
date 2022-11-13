import environ
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from accounts.utils import *
env = environ.Env()
environ.Env.read_env()


@login_required
def ServicesListView(request):
    services = Services.objects.all().order_by('-id')
    services = get_pagination(request, services)
    return render(request, 'services/services-list.html', {"head_title":"Services Management", "services":services})


@login_required
def AddServiceView(request):
    if request.method == 'POST':
        if Services.objects.filter(name=request.POST.get('name')):
            messages.error(request, 'Service with a same name already exist.')
            return redirect('services:services_list')
        else:
            service = Services.objects.create(
                name = request.POST.get('name'),
                image = request.FILES.get('image'),
                description = request.POST.get('description')
            )
            messages.success(request, 'Service Added Successfully!')
            return redirect('services:view_service', service.id)


@login_required
def ViewService(request, id):
    service = Services.objects.get(id=id)
    return render(request, 'services/view-service.html', {"service":service, 'head_title':"Services Management"})


@login_required
def DeleteService(request, id):
    service = Services.objects.get(id=id).delete()
    messages.success(request, 'Service Deleted Successfully!')
    return redirect('services:services_list')





