from django.urls import path
from . import views

urlpatterns = [
    path('groups/manager/users', views.ManagerUserViewSet.as_view({'get':'list'}), name='manager-users'),
    path('groups/manager/users/<int:pk>', views.ManagerUserViewSet.as_view({'get':'list'}), name='manager-users-detail'),
    path('groups/delivery-crew/users', views.DeliveryCrewUserViewSet.as_view({'get':'list'}), name='delivery-crew-users'),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewUserViewSet.as_view({'get':'list'}), name='delivery-crew-users-detail'),
    path('categories', views.CategoryViewSet.as_view({'get':'list'}), name='categories'),
    path('menu-items', views.MenuItemViewSet.as_view({'get':'list'}), name='menu-items'),
    path('menu-items/<int:pk>', views.MenuItemViewSet.as_view({'get':'list'}), name='menu-items-detail'),
    path('cart/menu-items', views.CartViewSet.as_view({'get':'list'}), name='cart'),
    path('cart/menu-items/<int:pk>', views.CartViewSet.as_view({'get':'list'}), name='cart-detail'),
    path('orders', views.OrderViewSet.as_view({'get':'list'}), name='orders'),
    path('orders/<int:pk>', views.OrderViewSet.as_view({'get':'list'}), name='orders-detail'),
    # path('order-items', views.OrderItemViewSet.as_view(), name='order-items'),
    # path('order-items/<int:pk>', views.OrderItemViewSet.as_view(), name='order-items-detail'),
]