with open('store/urls.py', 'r') as f:
    content = f.read()

admin_routes = """    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/products/', views.admin_products, name='admin_products'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/add-product/', views.admin_add_product, name='admin_add_product'),
    path('admin/edit-product/<int:product_id>/', views.admin_edit_product, name='admin_edit_product'),
    path('admin/delete-product/<int:product_id>/', views.admin_delete_product, name='admin_delete_product'),"""

content = content.replace(']', ',\n' + admin_routes + '\n]')

with open('store/urls.py', 'w') as f:
    f.write(content)

print('Updated successfully')
