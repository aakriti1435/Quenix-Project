from django.shortcuts import render,redirect
from accounts.constants import *
import logging
db_logger = logging.getLogger('db')


## Index Page
def index(request):
    if request.user.is_authenticated == True and request.user.is_superuser and request.user.role_id == ADMIN:
        return redirect('admin:index')
    else:
        return render(request, "frontend/index.html")


def handler404(request, exception, template_name="frontend/404.html"):
    db_logger.exception(Exception)
    return render(request, template_name, status=404)
    

def handler500(request, *args, **argv):
    db_logger.exception(Exception)
    return render(request, 'frontend/404.html', status=500)
    

def handler403(request, exception, template_name="frontend/404.html"):
    db_logger.exception(exception)
    return render(request, template_name, status=403)
    

def handler400(request, exception, template_name="frontend/404.html"):
    db_logger.exception(exception)
    return render(request, template_name, status=400)
    