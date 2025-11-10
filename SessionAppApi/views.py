from django.shortcuts import render
from rest_framework import viewsets
from SessionApp.models import Session
from .serializers import SessionsSerializer

# Create your views here.
class SessionViewSet(viewsets.ModelViewSet):
    queryset=Session.objects.all()
    serializer_class=SessionsSerializer
