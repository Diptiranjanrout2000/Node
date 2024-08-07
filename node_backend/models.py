from email.policy import default
from enum import unique
# from statistics import mode
from django.db import models
# from . models import *
from django.contrib.auth.models import User


class Node(models.Model):
    nodeid = models.CharField(max_length = 150)
    def __str__(self):
        return (self.nodeid)


class NodeModel(models.Model):
    node_id = models.ForeignKey(Node, on_delete=models.CASCADE)
    gateway_id = models.CharField(max_length=200, blank=True)
    data_field = models.JSONField(null=True, blank=True)

    def __str__(self):
         return (self.gateway_id)
    

    # def __str__(self):
    #     return f'NodeModel: {self.node_id}'
    
    # def add_data_field(self, key, value):
    #         if self.data is None:
    #             self.data = {}
    #         self.data[key] = value
    #         self.save()
    
    # def get_data_field(self, key):
    #     return self.data.get(key) if self.data else None