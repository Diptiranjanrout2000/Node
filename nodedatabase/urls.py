from django.contrib import admin
from django.urls import path,include
from node_backend import views

urlpatterns = [
    path('post_node/', views.post_node),
    path('get_node/',views.get_node),
    path('update_node/<int:nodeid>/',views.update_node),
    path('delete_node/<int:nodeid>/', views.delete_node),
    path('nodedata_get/', views.node_data_get_all),
    path('nodedata_post/',views.node_data_post),
    path('nodedata_last/', views.node_data_get),
    path('nodedata_100/', views.node_data_multiple),  
    path('update_node_data/<int:node_id>/', views.update_node_data),
    path('delete_node_data/<int:node_id>/', views.delete_node_data),
    path('admin/', admin.site.urls),

]
