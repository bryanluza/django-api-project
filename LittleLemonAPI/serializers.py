from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'menuitem_id', 'quantity', 'unitprice', 'price']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    delivery_crew = UserSerializer(read_only=True)
    delivery_crew_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'delivery_crew_id', 'status', 'total', 'date']

# class OrderItemSerializer(serializers.ModelSerializer):
#     order = OrderSerializer(read_only=True)
#     menuitem = MenuItemSerializer(read_only=True)
#     menuitem_id = serializers.IntegerField(write_only=True)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ['id', 'order', 'menuitem', 'menuitem_id', 'quantity', 'unitprice', 'price']
