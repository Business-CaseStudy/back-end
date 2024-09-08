from django.shortcuts import render
from rest_framework import viewsets
from .models import Investor
from .serializers import InvestorSerializer

# Create your views here.
class InvestorViewSet(viewsets.ModelViewSet):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer