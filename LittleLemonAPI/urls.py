from django.urls import path
from . import views
from djoser.views import UserViewSet

urlpatterns = [
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

    path('categories', views.CategoryViewSet.as_view({'get':'list'}), name='categories'),
    path('menu-items', views.MenuItemViewSet.as_view({'get':'list'}), name='menu-items'),
    path('menu-items/<int:pk>', views.MenuItemViewSet.as_view({'get':'list'}), name='menu-items-detail'),

    path('cart/menu-items', views.CartViewSet.as_view({'get':'list'}), name='cart'),
    path('cart/menu-items/<int:pk>', views.CartViewSet.as_view({'get':'list'}), name='cart-detail'),

    path('orders', views.OrderViewSet.as_view({'get':'list'}), name='orders'),
    path('orders/<int:pk>', views.OrderViewSet.as_view({'get':'list'}), name='orders-detail'),

    # Include the default Djoser user endpoints
    path('users/', UserViewSet.as_view({'post': 'create'}), name='user-list'),
    # Your custom 'me' endpoint
    path('users/me/', views.CustomUserViewSet.as_view({'get': 'me'}), name='user-me'),
]