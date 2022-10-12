from django.db.models.query_utils import Q
from accounts.models import *
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from .serializers import *
from django.contrib.auth import authenticate,logout
from rest_framework import views,response,status,permissions
import random
from django.contrib.auth.hashers import make_password


class CitiesListView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *ags , **kwargs):
        cities = Cities.objects.all()
        return Response({
            "data":CitySerializer(cities,many=True,context={"request":request}).data,
            "url":request.path,
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK)