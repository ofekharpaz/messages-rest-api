"""
URL configuration for messages-rest-api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from django.urls import path
from messages.views import write_message, get_user_messages, get_unread_messages, read_message, delete_message, signup, login

urlpatterns = [
    path('api/signup/', signup, name='signup'),
    path('api/login/', login, name='login'),
    path('api/write_message/', write_message, name='write_message'),
    path('api/user/<str:username>/messages/', get_user_messages, name='user_messages'),
    path('api/user/<str:username>/unread-messages/', get_unread_messages, name='unread_messages'),
    path('api/user/<str:username>/messages/read/', read_message, name='read_message'),
    path('api/user/<str:username>/messages/<str:subject>/delete/', delete_message, name='delete_message')
    # Add other URL patterns for different API endpoints
]