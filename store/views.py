"""Views for the `store` application.

Views are small function-based views intended for clarity. For larger apps
consider switching to class-based views or Django REST Framework endpoints.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .utils import get_cart, save_cart


def home(request):
    return redirect('product_list')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    """Add a product to the session cart.

    This keeps the endpoint idempotent and protects against invalid quantities.
    """

    product = get_object_or_404(Product, id=product_id)

    quantity = 1
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1

    # Normalize quantity and guard stock
    quantity = max(1, quantity)
    if product.stock < quantity:
        quantity = product.stock

    cart = get_cart(request.session)
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    save_cart(request.session, cart)

    product.stock -= quantity
    product.save()

    return redirect('cart')


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request.session)

    if str(product_id) in cart:
        quantity_in_cart = cart[str(product_id)]
        product.stock += quantity_in_cart
        product.save()

        del cart[str(product_id)]
        save_cart(request.session, cart)

    return redirect('cart')


def update_cart_item(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = get_cart(request.session)

        try:
            new_quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            new_quantity = 1

        new_quantity = max(1, new_quantity)

        if str(product_id) in cart:
            old_quantity = cart[str(product_id)]
            quantity_diff = new_quantity - old_quantity

            if quantity_diff > 0 and product.stock < quantity_diff:
                new_quantity = old_quantity + product.stock
                quantity_diff = product.stock

            product.stock -= quantity_diff
            product.save()

            cart[str(product_id)] = new_quantity
            save_cart(request.session, cart)

    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            is_completed=True
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
            # Stock already decremented when added to cart

        request.session['cart'] = {}

        return render(request, 'store/order_success.html', {
            'order': order
        })

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()

    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('product_list')

# Admin Views
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('product_list')
    
    from django.contrib.auth.models import User
    from django.db.models import Sum
    
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_users = User.objects.count()
    
    products = Product.objects.all().order_by('-id')
    orders = Order.objects.all().order_by('-id')
    
    return render(request, 'store/admin_dashboard.html', {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'products': products,
        'orders': orders,
    })


@login_required
def admin_products(request):
    if not request.user.is_staff:
        return redirect('product_list')
    
    products = Product.objects.all().order_by('-id')
    return render(request, 'store/admin_products.html', {'products': products})


@login_required
def admin_orders(request):
    if not request.user.is_staff:
        return redirect('product_list')
    
    orders = Order.objects.all().order_by('-id')
    return render(request, 'store/admin_orders.html', {'orders': orders})


@login_required
def admin_users(request):
    if not request.user.is_staff:
        return redirect('product_list')
    
    from django.contrib.auth.models import User
    users = User.objects.all().order_by('-id')
    return render(request, 'store/admin_users.html', {'users': users})


@login_required
def admin_add_product(request):
    if not request.user.is_staff:
        return redirect('product_list')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.POST.get('image')
        
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            stock=stock,
            image=image
        )
        return redirect('admin_products')
    
    return render(request, 'store/admin_add_product.html')


@login_required
def admin_edit_product(request, product_id):
    if not request.user.is_staff:
        return redirect('product_list')
    
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.image = request.POST.get('image')
        product.save()
        return redirect('admin_products')
    
    return render(request, 'store/admin_edit_product.html', {'product': product})


@login_required
def admin_delete_product(request, product_id):
    if not request.user.is_staff:
        return redirect('product_list')
    
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_products')
