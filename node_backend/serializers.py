from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'

class NodeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeModel
        fields = '__all__'