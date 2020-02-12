from django.shortcuts import render
from rest_framework import viewsets
from .models import Header, Application
from .serializers import HeaderSerializer, ApplicationSerializer

class HeaderView(viewsets.ModelViewSet):
    queryset = Header.objects.all()
    serializer_class = HeaderSerializer

class ApplicationView(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
