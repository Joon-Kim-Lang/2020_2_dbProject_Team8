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
from django.contrib import admin
from django.urls import path, include

from administrator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submitter/', include('submitter.urls')),

    # ==========================
    # ADMINISTRATOR URL PATTERNS
    # ==========================

    # ===================== JH ======================
    path('api/register/', views.register),
    path('api/task/create/', views.createTask),
    path('api/login/', views.login),
    path('api/getinfo/', views.getinfo),
    path('api/logout/', views.logout),
    path('api/member/search/', views.searchmember),
    path('api/member/info/', views.memberinfo),
    path('api/task/newodt/', views.addODT),
    path('api/user/info/', views.userinfo),
    path('api/user/modify/', views.modifyuser),
    path('api/user/delete/', views.deleteuser),

    # ===================== HJ ======================
    path('api/adminmain/', views.adminMain),
    path('api/task/administrate/', views.taskAdministration),
    path('api/task/statistics/', views.taskStatistics),
    path('api/task/now/', views.taskNow),

    # ===================== HM ======================
    path('api/task/manage/', views.manageMain),
    path('api/member/allow/', views.addParticipant),
    path('api/task/allowodt/', views.addDatatype),
    path('api/task/setpass/', views.setPassval),
    path('api/task/getmember/', views.getWaitingMember),
    path('api/task/getodt/', views.getWaitingODT)
]
