import re
import environ
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        return render(request,'frontend/login.html' , {'activated' : 'login', "title":"Login"})
    
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
            return render(request, 'frontend/login.html',{"email":email})
        
        if user.is_superuser and user.role_id == ADMIN:
            login(request, user)
            messages.error(request, 'Login Successfully!')
            return redirect('admin:index')
        else:
            history.status = LOGIN_FAILURE
            history.save()
            messages.error(request, 'Invalid login credentials')
            return render(request, 'frontend/login.html',{"email":email})


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
    loginhistory = LoginHistory.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(loginhistory, PAGE_SIZE)
    try:
        loginhistory = paginator.page(page)
    except PageNotAnInteger:
        loginhistory = paginator.page(1)
    except EmptyPage:
        loginhistory = paginator.page(paginator.num_pages)
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