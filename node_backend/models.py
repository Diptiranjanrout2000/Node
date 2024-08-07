from enum import unique
# from statistics import mode
from djongo import models
from django.contrib.auth.models import User
# Create your models here.

class Node(models.Model):
    nodeid = models.CharField(max_length = 150)
    

    def __str__(self):
        return (self.id)

class NodeModel(models.Model):
    node_id = models.ForeignKey(Node,on_delete=models.CASCADE,unique=True)
    gateway_id = models.CharField(max_length=200, blank=True)
    data = models.JSONField(default=dict,blank=True) 

    def __str__(self):
        return f'NodeModel: {self.node_id.nodeid}'
    
    def add_data_field(self, key, value):
        self.data[key] = value
        self.save()

    def get_data_field(self, key):
        return self.data.get(key)