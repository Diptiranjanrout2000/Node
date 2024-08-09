from email.policy import default
from enum import unique
# from statistics import mode
from django.db import models
# from . models import *
from django.contrib.auth.models import User


class Node(models.Model):
    nodeid = models.CharField(max_length = 150,primary_key=True)
    def __str__(self):
        node = f"{self.nodeid}"
        return node


class NodeModel(models.Model):
    node_id = models.ForeignKey(Node, on_delete=models.CASCADE)
    gateway_id = models.CharField(max_length=200, blank=True,primary_key=True)
    data_field = models.JSONField(null=True, blank=True)

    def __str__(self):
         gateway = f"{self.gateway_id}"
         return gateway
    

    # def __str__(self):
    #     return f'NodeModel: {self.node_id}'
    
    # def add_data_field(self, key, value):
    #         if self.data is None:
    #             self.data = {}
    #         self.data[key] = value
    #         self.save()
    
    # def get_data_field(self, key):
    #     return self.data.get(key) if self.data else None