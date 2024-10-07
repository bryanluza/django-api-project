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
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    unitprice = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        read_only=True
    )
    price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Cart
        fields = ['id', 'menuitem', 'menuitem_id', 'quantity', 'unitprice', 'price']
        read_only_fields = ['id', 'unitprice', 'price']

    def create(self, validated_data):
        menuitem_id = validated_data['menuitem_id']
        menuitem = MenuItem.objects.get(id=menuitem_id)
        quantity = validated_data['quantity']

        # Assuming unitprice is a field on MenuItem model
        unitprice = menuitem.price  # Adjust this if the field name is different
        price = unitprice * quantity

        cart_item = Cart.objects.create(
            menuitem=menuitem,
            quantity=quantity,
            user=self.context['request'].user  # Assuming you're passing the request in the context
        )
        return cart_item


    def update(self, instance, validated_data):
        if 'quantity' in validated_data:
            instance.quantity = validated_data['quantity']
            instance.price = instance.unitprice * instance.quantity
        return super().update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    delivery_crew = UserSerializer(read_only=True)
    delivery_crew_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'delivery_crew_id', 'status', 'total', 'date']

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem_title = serializers.ReadOnlyField(source='menuitem.title')
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'menuitem_title', 'quantity', 'unitprice', 'price']
        read_only_fields = ['unitprice']

    def create(self, validated_data):
        menuitem = validated_data['menuitem']
        validated_data['unitprice'] = menuitem.price
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'menuitem' in validated_data:
            menuitem = validated_data['menuitem']
            instance.unitprice = menuitem.price
        return super().update(instance, validated_data)

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['delivery_crew', 'status']
        read_only_fields = ['id', 'user', 'total', 'date']

    def validate(self, data):
        user = self.context['request'].user
        if user.groups.filter(name='Delivery Crew').exists():
            if 'delivery_crew' in data:
                raise serializers.ValidationError("Delivery crew cannot update the delivery_crew field.")
        return data
