from rest_framework import viewsets, status,  permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from djoser.views import UserViewSet
from .models import *
from .serializers import *
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import get_object_or_404

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

# Create your views here.
# User management views
class CustomUserViewSet(UserViewSet):
    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

class ManagerUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def get_queryset(self):
        managers_group = Group.objects.get(name='Manager')
        return User.objects.filter(groups=managers_group)

    @action(detail=False, methods=['post'])
    def assign_manager(self, request):
        username = request.data.get('username')
        user_id = request.data.get('user_id')

        if not username and not user_id:
            return Response({"error": "Either username or user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if username:
                user = User.objects.get(username=username)
            else:
                user = User.objects.get(id=user_id)
            manager_group, _ = Group.objects.get_or_create(name='Manager')
            if manager_group in user.groups.all():
                return Response({"message": f"User '{user.username}' is already a manager"}, status=status.HTTP_200_OK)
            user.groups.add(manager_group)
            return Response({
                "message": f"User '{user.username}' has been successfully assigned as a manager",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def remove_manager(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            manager_group = Group.objects.get(name='Manager')
            if manager_group not in user.groups.all():
                return Response({"message": f"User '{user.username}' is not a manager"}, status=status.HTTP_400_BAD_REQUEST)
            user.groups.remove(manager_group)
            return Response({"message": f"User '{user.username}' has been removed from the manager group"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class DeliveryCrewUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def get_queryset(self):
        delivery_crew_group = Group.objects.get(name='Delivery Crew')
        return User.objects.filter(groups=delivery_crew_group)

    @action(detail=False, methods=['post'])
    def assign_delivery_crew(self, request):
        username = request.data.get('username')
        user_id = request.data.get('user_id')

        if not username and not user_id:
            return Response({"error": "Either username or user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if username:
                user = User.objects.get(username=username)
            else:
                user = User.objects.get(id=user_id)
            delivery_crew_group, _ = Group.objects.get_or_create(name='Delivery Crew')
            if delivery_crew_group in user.groups.all():
                return Response({"message": f"User '{user.username}' is already part of the Delivery Crew"}, status=status.HTTP_200_OK)
            user.groups.add(delivery_crew_group)
            return Response({
                "message": f"User '{user.username}' has been successfully assigned to the Delivery Crew",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def remove_delivery_crew(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            delivery_crew_group = Group.objects.get(name='Delivery Crew')
            if delivery_crew_group not in user.groups.all():
                return Response({"message": f"User '{user.username}' is not part of the Delivery Crew"}, status=status.HTTP_400_BAD_REQUEST)
            user.groups.remove(delivery_crew_group)
            return Response({"message": f"User '{user.username}' has been removed from the Delivery Crew"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Model views
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsManager())

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        # Delete all cart items for the current user
        deleted_count, _ = Cart.objects.filter(user=self.request.user).delete()
        if deleted_count > 0:
            return Response({"message": f"Successfully deleted {deleted_count} item(s) from your cart."},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Your cart is already empty."},
                            status=status.HTTP_404_NOT_FOUND)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew_id=self.request.user)
        else:
            return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(user=request.user, total=0, date=timezone.now())
            total = 0
            for cart_item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    menuitem=cart_item.menuitem,
                    quantity=cart_item.quantity,
                    unitprice=cart_item.menuitem.price
                )
                total += order_item.quantity * order_item.unitprice
                cart_item.delete()

            order.total = total
            order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs.get('pk')
        if self.request.user.groups.filter(name='Manager').exists():
            return OrderItem.objects.filter(order_id=order_id)
        else:
            return OrderItem.objects.filter(order_id=order_id, order__user=self.request.user)

    def list(self, request, *args, **kwargs):
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id)

        if not self.request.user.groups.filter(name='Manager').exists() and order.user != request.user:
            return Response({"detail": "You do not have permission to view this order's items."},
                            status=status.HTTP_403_FORBIDDEN)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id)

        # Check if the user is in the Manager group
        if not self.request.user.groups.filter(name='Manager').exists():
            return Response({"detail": "You do not have permission to delete this order."},
                            status=status.HTTP_403_FORBIDDEN)
        # Delete all related OrderItems
        OrderItem.objects.filter(order=order).delete()
        # Delete the Order
        order.delete()
        return Response({"detail": "Order and related items have been deleted."},
                        status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        return self._update_order(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self._update_order(request, *args, partial=True, **kwargs)

    def _update_order(self, request, *args, partial=False, **kwargs):
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id)

        is_manager = self.request.user.groups.filter(name="Manager").exists()
        is_delivery_crew = self.request.user.groups.filter(name="Delivery Crew").exists()
        is_assigned_delivery_crew = is_delivery_crew and Order.objects.filter(id=order_id, delivery_crew=self.request.user).exists()

        if not (is_manager or is_assigned_delivery_crew):
            return Response({"detail": "You do not have permission to update this order."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = OrderUpdateSerializer(order, data=request.data, partial=partial, context={'request': request})

        if serializer.is_valid():
            if is_delivery_crew:
                # Delivery crew can only update the status field
                if set(request.data.keys()) - {'status'}:
                    return Response({"detail": "Delivery crew can only update the status field."},
                                    status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


