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
    pass
