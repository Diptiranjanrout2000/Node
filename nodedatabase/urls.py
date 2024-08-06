"""
URL configuration for nodedatabase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from node_backend import views

urlpatterns = [
    path('post_node/', views.post_node),
    path('get_node/',views.get_node),
    path('update_node/<int:nodeid>/',views.update_node),
    path('delete_node/<int:nodeid>/', views.delete_node),
    path('nodedata_get/', views.node_data_get),
    path('nodedata_post/',views.node_data_post),
    path('update_node_data/<int:node_id>/', views.update_node_data),
    path('delete_node_data/<int:node_id>/', views.delete_node_data),
    path('', admin.site.urls),

]
