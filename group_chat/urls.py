# admin_module/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/list/', views.list_groups, name='list_groups'),#group details
    path('groups/<int:group_id>/', views.get_group_details, name='get_group_details'),#get perticular group details

    path('groups/<int:group_id>/update/', views.update_group, name='update_group'),#update group details
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('groups/<int:group_id>/send_message/', views.send_message_to_group, name='send_message_to_group'),#send message in group 
    path('groups/<int:group_id>/add_member/', views.add_member_to_group, name='add_member_to_group'),
    path('groups/<int:group_id>/remove_member/', views.remove_member_from_group, name='remove_member_from_group'),
    
    path('groups/<int:group_id>/messages/', views.get_group_messages, name='get_group_messages'),
    path('messages/<int:message_id>/like_message/', views.like_unlike_message, name='like_unlike_message'),#like or unlike message
]
