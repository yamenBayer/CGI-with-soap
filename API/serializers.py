from rest_framework import serializers
from API.models import *


class Face_CollectionSerializer(serializers.ModelSerializer):
 class Meta:
    model = Face_Collection
    fields = ['id', 'name','created_at','api_key']

class ServicesSerializer(serializers.ModelSerializer):
 class Meta:
    model = Services
    fields = ['id', 'name','type','api_key','status','socket_ip','live_type']
    