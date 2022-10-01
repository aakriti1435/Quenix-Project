import os
from django.db import models
from django.utils import timezone
from django.http import HttpResponse
from django.utils.encoding import smart_str



class Backup(models.Model):
    name = models.CharField( max_length=255,null=True, blank=True)
    size = models.CharField(max_length=255,null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    is_schema = models.BooleanField(default=False)

    @classmethod
    def Downloadfile(zips,path,file_name):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path= os.path.join(BASE_DIR)

        file_path = f"{path}/backup/sql_files/{file_name}"
        filepath= file_path
        with open(filepath, 'r') as f:
            response = HttpResponse(f.read(),content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
            response['X-Sendfile'] = smart_str(path)
        return response
