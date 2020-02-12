from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('headers', views.HeaderView)
router.register('applications', views.ApplicationView)

urlpatterns = [
    path('', include(router.urls))
]