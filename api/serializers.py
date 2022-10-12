from rest_framework.serializers import ModelSerializer
from accounts.models import *

class CitySerializer(ModelSerializer):

    class Meta:
        model = Cities
        fields = ('id','city')