from rest_framework import viewsets
from .models import *
from .serializers import *
from django.contrib.auth.models import User

# Create your views here.
# User management views
class ManagerUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer

class DeliveryCrewUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Model views
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# class OrderItemViewSet(viewsets.ModelViewSet):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer