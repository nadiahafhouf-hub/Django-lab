from rest_framework import serializers
from SessionApp.models import Session

class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Session
        fields ='__all__' #appele a tout les fields au lieu de qlq une
        

