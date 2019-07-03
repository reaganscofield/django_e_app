from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

from .serializers import ( 
    SerializersProducts, SerializersUsers, 
    SerializersAddCard, SerializersBought 
)

from .models import Products, Users, AddCard, Bought

router = routers.DefaultRouter()

router.register('products', views.ProductSerializer)
router.register('add_card', views.AddCardView)
router.register('bought', views.BoughtView)
router.register(r'^/test/', views.BoughtList.as_view(queryset=Bought.objects.all(), serializer_class=SerializersBought), name='bought-list')

urlpatterns = [
    path('', include(router.urls)),
]
