import os
import time
from django.shortcuts import render ,redirect
from accounts.constants import PAGE_SIZE
from .models import *
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import environ
from django.contrib.auth.decorators import login_required
env = environ.Env()
environ.Env.read_env()


@login_required
def backup(request):
	backup = Backup.objects.all().order_by('-created_on')
	page = request.GET.get('page', 1)
	paginator = Paginator(backup, PAGE_SIZE)
	try:
		backup = paginator.page(page)
	except PageNotAnInteger:
		backup = paginator.page(1)
	except EmptyPage:
		backup = paginator.page(paginator.num_pages)
	return render(request, "backup/backup.html",{"backup":backup,"head_title":"Backup"})


@login_required
def downloadFile(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	path= os.path.join(BASE_DIR)
	backup = Backup.objects.get(id=request.GET.get("id"))
	file_name = backup.name
	file_path = f"{path}/backup/sql_files/{file_name}"
	filepath= file_path
	with open(filepath, 'r') as f:
		response = HttpResponse(f.read(), content_type='application')
		response['Content-Disposition'] = 'inline; filename=' + file_name
	return Backup.Downloadfile(response,file_name)


@login_required
def database_backup(request):
	username = env('LOCAL_DB_USERNAME')
	password = env('LOCAL_DB_PASSWORD')
	database = env('LOCAL_DB_NAME')
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	path= os.path.join(BASE_DIR)
	BACKUP_PATH = f'{path}/backup/sql_files/'
	DATETIME = time.strftime('%Y%m%d-%H%M%S')
	TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME
	dumpcmd = "mysqldump -h " + "localhost" + " -u " + username + " -p" + password + " " + database + " > " + BACKUP_PATH + "/" + database+DATETIME + ".sql"
	os.system(dumpcmd)
	value = Backup.objects.create(
		name = database+DATETIME + ".sql",
		size = os.path.getsize(f"{path}/backup/sql_files/"+database+DATETIME + ".sql"),
		is_schema = False
	)
	messages.add_message(request, messages.INFO, 'Database backup created successfully!')
	return redirect('backup:backup')


@login_required
def database_schema(request):	
	username = env('LOCAL_DB_USERNAME')
	password = env('LOCAL_DB_PASSWORD')
	database = env('LOCAL_DB_NAME')
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	path= os.path.join(BASE_DIR)
	SCHEMA_PATH = f'{path}/backup/sql_files/'
	DATETIME = time.strftime('%Y%m%d-%H%M%S')
	TODAYBACKUPPATH = SCHEMA_PATH + '/' + DATETIME
	dumpcmd = "mysqldump -h " + "localhost" + " -u " + username + " -p" + password + " --no-data " + database + " > " + SCHEMA_PATH + "/" + database+DATETIME + ".sql"
	os.system(dumpcmd)
	value = Backup.objects.create(
		name = database+DATETIME + ".sql",
		size = os.path.getsize(f"{path}/backup/sql_files/"+database+DATETIME + ".sql"),
		is_schema = True
	)
	messages.add_message(request, messages.INFO, 'Database structure created successfully!')
	return redirect('backup:backup')


@login_required
def DeleteBackup(request):
    if request.method == 'GET':
        backup = Backup.objects.get(id=request.GET.get("id"))
        if backup.is_schema:
            messages.add_message(request, messages.INFO, 'Database structure deleted successfully!')
        else:
            messages.add_message(request, messages.INFO, 'Database backup deleted successfully!')
        if backup:
            backup.delete()
        return redirect('backup:backup')