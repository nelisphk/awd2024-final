from rest_framework import serializers
from .models import *

class Details_list(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['pk', 'user', 'image']