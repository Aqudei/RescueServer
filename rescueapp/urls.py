"""rescue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from .viewset import PersonViewSet, CenterViewSet, HouseholdViewSet
from .views import ImageAPIView

router = routers.DefaultRouter()
router.register(r'people', PersonViewSet, base_name='person')
router.register(r'centers', CenterViewSet, base_name='center')
router.register(r'households', HouseholdViewSet, base_name='household')
urlpatterns = router.urls
urlpatterns += [url(r'^upload/(\d+)', ImageAPIView.as_view()), ]
