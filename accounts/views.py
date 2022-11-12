import re
import environ
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from frontend.views import *
from .models import *
from django.db.models import Q
from django.db.models import Count
from .backend import authenticate
from .utils import *
env = environ.Env()
environ.Env.read_env()


class AdminLoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect('accounts:login')

      
class LogOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('accounts:login')


class LoginView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'frontend/login-signup.html' , {'activated' : 'login', "title":"Login"})
    
    def post(self,request,*args,**kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")

        history = LoginHistory.objects.create(
            user_ip = request.META.get("REMOTE_ADDR"),
            user_agent = request.META['HTTP_USER_AGENT'],
            code = "http://" + request.META.get("REMOTE_ADDR") + request.path,
            user = request.POST.get("email")
        )
        if request.POST.get('remember_me')=='on':    
            request.session.set_expiry(7600) 
        user = authenticate(username=email, password=password)
        if not user:
            history.status = LOGIN_FAILURE
            history.save()
            messages.error(request, 'Invalid login credentials')
            return render(request, 'frontend/login-signup.html',{"email":email})
        
        if user.is_superuser and user.role_id == ADMIN:
            login(request, user)
            messages.error(request, 'Login Successfully!')
            return redirect('admin:index')
        else:
            history.status = LOGIN_FAILURE
            history.save()
            messages.error(request, 'Invalid login credentials')
            return render(request, 'frontend/login-signup.html',{"email":email})


@login_required
def EditUser(request,id):
    user=User.objects.get(id=id)
    if request.method == 'POST':
        if request.POST.get('username'):
            user.username = request.POST.get('username')
        if request.POST.get('full_name'):
            user.full_name = request.POST.get('full_name')
        if request.POST.get('email'):
            user.email = request.POST.get('email')
        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES.get('profile_pic')
        user.save()
        messages.success(request, 'Profile Updated successfully')
        return redirect('accounts:view_user', id=user.id)
    return render(request, 'admin/edit-user.html',{"user":user})


@login_required
def ViewUser(request,id):
    user=User.objects.get(id=id)
    return render(request, 'admin/profile.html', {'user':user, "head_title":"Profile"})


class PasswordChange(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        return render(request,'admin/change-password.html',{"head_title":"Change Password"})

    def post(self,request,*args,**kwargs):
        id=request.user.id
        user=User.objects.get(id=id)
        pass1 = request.POST.get("password")
        user.set_password(pass1)
        user.save()
        messages.add_message(request, messages.INFO, 'Password changed successfully')
        return redirect('accounts:login')


@login_required
def LoginHistoryView(request):
    loginhistory = get_pagination(request, LoginHistory.objects.all().order_by('-id'))
    return render(request, 'admin/login-history.html', {"loginhistory":loginhistory, "head_title":"Login History"})


@login_required
def DeleteHistory(request):
    history=LoginHistory.objects.all()
    if history:
        history.delete()
        messages.success(request,"All Login History Cleared Sucessfully!!!")
    else:
        messages.error(request,"Nothing to Delete!!!")
    return redirect('accounts:login_history')


@login_required
def CitiesList(request):
    cities = get_pagination(request, Cities.objects.all().order_by('-id'))
    return render(request, "admin/cities.html", {"head_title":"Cities Management", "cities":cities})


@login_required
def UserGraph(request):
    if request.is_ajax:
        customers, service_providers = [],[]
        months = {'jan':'1','feb':'2','mar':'3','apr':'4','may':'5','jun':'6','jul':'7','aug':'8','sep':'9','oct':'10','nov':'11','dec':'12'}
        for i in months.keys():
            customers.append(User.objects.filter(role_id = CUSTOMER,created_on__year=str(datetime.now().year),created_on__month= months[i]).count())
            service_providers.append(User.objects.filter(role_id = SERVICE_PROVIDER,created_on__year=str(datetime.now().year),created_on__month= months[i]).count())

        chart = {
            'chart': {'type': 'column'},
            'title': {'text': f'User Records in {datetime.now().year}'},
            'xAxis': { 'categories': [i.upper() for i in months.keys()]},
            'colors': ['#3b7ff2', '#fe7096'],
            'series': [{
                    'name': 'Customers',
                    'data':customers
                },
                {
                    'name': 'Service Providers',
                    'data':service_providers
                }]
            }
        return JsonResponse(chart)


@login_required
def CustomersList(request):
    users = User.objects.filter(role_id=CUSTOMER).order_by('-id')
    users = get_pagination(request, users)
    return render(request, 'users/customers-list.html', {"head_title":"Customers Management", "users":users})


@login_required
def ServiceProvidersList(request):
    users = User.objects.filter(role_id=SERVICE_PROVIDER).order_by('-id')
    users = get_pagination(request, users)
    return render(request, 'users/serviceproviders-list.html', {"head_title":"Service PRoviders Management", "users":users})


@login_required
def ChangeStatusActive(request, id):
    user = User.objects.get(id=id)
    user.status = ACTIVE
    user.is_active = True
    user.save()
    messages.success(request, 'User Account Activated Successfully!')
    return redirect('accounts:view_user',user.id)


@login_required
def ChangeStatusInActive(request, id):
    user = User.objects.get(id=id)
    user.status = INACTIVE
    user.is_active = False
    user.save()
    messages.success(request, 'User Account Deactivated Successfully!')
    return redirect('accounts:view_user',user.id)


@login_required
def ChangeStatusDelete(request, id):
    user = User.objects.get(id=id)
    user.status = DELETED
    user.is_active = False
    user.save()
    messages.success(request, 'User Account Deleted Successfully!')
    return redirect('accounts:view_user',user.id)