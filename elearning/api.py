from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework import mixins

from .models import *
from .serializers import * 

class Details(generics.ListAPIView):
    queryset = AppUser.objects.all()
    serializer_class = Details_list