from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path('',get_all_node_data)
 
]