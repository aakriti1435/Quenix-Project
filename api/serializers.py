from rest_framework.serializers import ModelSerializer,SerializerMethodField
from accounts.models import *
from rest_framework.authtoken.models import Token


class UserSerializer(ModelSerializer):
    token = SerializerMethodField(read_only = True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'full_name', 'dob', 'gender', 'email', 'mobile_no', 'profile_pic', 'role_id', 'status', 'created_on', 'service_role', 'temp_otp', 'lattitude', 'longitude', 'token')
        
    def get_token(self, obj):
        try:
            token = Token.objects.get(user = obj)
        except:
            token = None
        return token.key if token else ""


class CitySerializer(ModelSerializer):

    class Meta:
        model = Cities
        fields = ('id','city')