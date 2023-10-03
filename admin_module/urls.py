from django.urls import path
from .views import user_registration, user_edit, user_login, user_logout,get_all_users

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register_user/', user_registration, name='register'),#create user api
    path('edit_user/<int:id>/', user_edit, name='edit'),
    path('get_all_users/', get_all_users, name='get_all_users'),
    
]
