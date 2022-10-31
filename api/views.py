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

    def get(self, request, *args , **kwargs):
        cities = Cities.objects.all()
        return Response({
            "data":CitySerializer(cities,many=True,context={"request":request}).data,
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK)


class GenerateOTP(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args , **kwargs):
        if not request.data.get('mobile_no'):
            return Response({
                "message":"Please Enter Mobile Number",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
            
        if not request.data.get('role_id'):
            return Response({
                "message":"Please select a role id",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(Q(status=ACTIVE)|Q(status=INACTIVE),mobile_no=request.data.get('mobile_no'), role_id=request.data.get('role_id')):
            user = User.objects.filter(Q(status=ACTIVE)|Q(status=INACTIVE),mobile_no=request.data.get('mobile_no'), role_id=request.data.get('role_id')).last()
            
            if user.status == INACTIVE:
                return Response({
                    "message":"Your Account Is Inactive. Please Contact Admin",
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_400_BAD_REQUEST)
            user.temp_otp = str(random.randrange(100000, 999999))
            user.save()
        else:
            # if not request.data.get('city'):
            #     return response.Response({
            #     "message":"Please Select a City",
            #     "status":status.HTTP_400_BAD_REQUEST
            # },status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create(
                mobile_no=request.data.get('mobile_no'),
                role_id=request.data.get('role_id'),
                # city = Cities.objects.get(id=request.data.get('city')),
                # lattitude = request.data.get('lattitude'),
                # longitude = request.data.get('longitude'),
                temp_otp = str(random.randrange(100000, 999999))
            )
        try:
            token = Token.objects.get(user = user)
        except:
            token = Token.objects.create(user = user)
        try:
            device = Device.objects.get(user = user)
        except Device.DoesNotExist:
            device = Device.objects.create(user = user)
        device.device_type = request.data.get('device_type')
        device.device_name = request.data.get('device_name')
        device.device_token = request.data.get('device_token')
        device.save()    
        return Response({
            "message":str(user.temp_otp)+" Is Your OTP. Please Verify Your Mobile Number.",
            "data":UserSerializer(user,context={"request":request}).data,
            "status":status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)   
        
              
class VerifyOTP(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request, *args , **kwargs):  
        user = User.objects.get(id=request.user.id)
        if not request.data.get('otp'):
            return Response({
                "message":"Please enter OTP",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
        if user.temp_otp != request.data.get('otp'):
            return Response({
                "message":"Incorrect OTP.",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            user.temp_otp = ""
            user.save()
            return Response({
                "message":"Login Successful!" if user.is_profile_setup else "Phone Number Verified Successfully!",
                "data":UserSerializer(user,context={"request":request}).data,
                "status":status.HTTP_200_OK,
            }, status=status.HTTP_200_OK)
   
   
class SocialLogin(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args , **kwargs):
        if not request.data.get('social_id'):
            return Response({
                "message":"Please Enter Social Id",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('role_id'):
            return Response({
                "message":"Please Enter Role Id",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('email'):
            return Response({
                "message":"Please Enter Email",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
   
        if User.objects.filter(Q(status=ACTIVE)|Q(status=INACTIVE),social_id=request.data.get('social_id'), role_id=request.data.get('role_id')):
            user = User.objects.filter(Q(status=ACTIVE)|Q(status=INACTIVE),social_id=request.data.get('social_id'), role_id=request.data.get('role_id')).last()
            message = "Login Successfully!"
        else:
            user = User.objects.create(
                social_id = request.data.get('social_id'),
                role_id = request.data.get('role_id'),
                email = request.data.get('email'),
                social_type = GOOGLE_LOGIN
            )
            message = "Registration Done Successfully!"
        try:
            token = Token.objects.get(user = user)
        except:
            token = Token.objects.create(user = user)
        try:
            device = Device.objects.get(user = user)
        except Device.DoesNotExist:
            device = Device.objects.create(user = user)
        device.device_type = request.data.get('device_type')
        device.device_name = request.data.get('device_name')
        device.device_token = request.data.get('device_token')
        device.save() 
        return Response({
            "message":message,
            "data":UserSerializer(user,context={"request":request}).data,
            "status":status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)
            
   
class CheckUser(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        return Response({
            "data":UserSerializer(request.user,context={"request":request}).data,
            "status":status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)
      
      
class LogOutView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        Token.objects.filter(user = request.user).delete()
        Device.objects.filter(user = request.user).delete()     
        logout(request)   
        return Response({
            "message":"Logout Successfully!",
            "status":status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)
            
            
class UpdateProfile(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        
        if not request.data.get('first_name'):
            return Response({"message":"Please enter your first name","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('last_name'):
            return Response({"message":"Please enter your last name","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('email'):
            return Response({"message":"Please enter your email id","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('dob'):
            return Response({"message":"Please enter your date of birth","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('gender'):
            return Response({"message":"Please select your gender","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email = request.data.get('email'), status=ACTIVE, role_id=user.role_id).exclude(id=user.id):
            return Response({"message":"There is already registered user with this email address.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        user.email = request.data.get('email')
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.full_name = request.data.get('first_name') + " " + request.data.get('last_name')
        user.dob = request.data.get('dob')
        user.gender = request.data.get('gender')
        if request.data.get('password'):
            user.password = make_password(request.data.get('password')) 
        user.is_profile_setup = True
        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES.get('profile_pic')
        user.save()
        
        return Response({
            "message":"Profile Updated Successfully!",
            "data":UserSerializer(user, context={"request":request}).data,
            "status":status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)            
            
            
# class CheckCity(APIView):
#     permission_classes = (permissions.AllowAny, )
    
#     def get(self, request, *args, **kwargs):
#         if not request.query_params.get('')
        
        