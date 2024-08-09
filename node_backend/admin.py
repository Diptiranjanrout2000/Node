from django.contrib import admin

# Register your models here.
from .models import *
@admin.register(Node)
class Node(admin.ModelAdmin):
    list_display =['nodeid']

@admin.register(NodeModel)
class NodeModel(admin.ModelAdmin):
    list_display =['node_id','gateway_id','data_field']



# admin.site.register(NodeModel)
