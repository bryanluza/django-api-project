from rest_framework import viewsets, status,  permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from djoser.views import UserViewSet
from .models import *
from .serializers import *

# Maybe put this in a permissions.py file and inport it
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

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

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

# class OrderItemViewSet(viewsets.ModelViewSet):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer