from django.urls import path
from . import views


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:product_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/products/', views.admin_products, name='admin_products'),
    path('dashboard/orders/', views.admin_orders, name='admin_orders'),
    path('dashboard/users/', views.admin_users, name='admin_users'),
    path('dashboard/add-product/', views.admin_add_product, name='admin_add_product'),
    path('dashboard/edit-product/<int:product_id>/', views.admin_edit_product, name='admin_edit_product'),
    path('dashboard/delete-product/<int:product_id>/', views.admin_delete_product, name='admin_delete_product'),
]
