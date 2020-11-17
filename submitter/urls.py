"""dbProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from .import views

app_name = 'submitter'
urlpatterns = [
    path('submitMain/', views.submitMain, name = 'submitMain'),
    path('submitMain/task-<int:taskid>/detail', views.taskDetail, name='taskDetail'),
    path('submitMain/task-<int:taskid>/apply', views.taskApply, name='taskApply'),
]
