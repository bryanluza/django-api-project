from django.urls import path, include
from rest_framework import routers
from . import views
from djoser.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'menu-items', views.MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('groups/manager/users', views.ManagerUserViewSet.as_view({
        'get':'list',
        'post':'assign_manager'
        }), name='manager-users'),
    path('groups/manager/users/<int:pk>', views.ManagerUserViewSet.as_view({
        'delete' : 'remove_manager',
        }), name='manager-users-delete'),
    path('groups/delivery-crew/users', views.DeliveryCrewUserViewSet.as_view({
        'get':'list',
        'post':'assign_delivery_crew'
        }), name='delivery-crew-users'),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewUserViewSet.as_view({
        'delete' : 'remove_delivery_crew'
        }), name='delivery-crew-users-delete'),
    path('cart/menu-items/', views.CartViewSet.as_view({
        'get': 'list',
        'post': 'perform_create',
        'delete': 'destroy'
    }), name='cart'),

    path('orders', views.OrderViewSet.as_view({'get':'list'}), name='orders'),
       path('orders/<int:pk>', views.OrderViewSet.as_view({'get':'list'}), name='orders-detail'),

    # Default Djoser user endpoints
    path('users/', UserViewSet.as_view({'post': 'create'}), name='user-list'),
    # Custom 'me' endpoint
    path('users/me/', views.CustomUserViewSet.as_view({'get': 'me'}), name='user-me'),
]