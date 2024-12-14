from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from Payment.models import Payment
from django.contrib.auth.decorators import login_required
from orders.models import Product
from django.db import transaction
from django.http import HttpResponseBadRequest

from .models import Order, OrderItem, Product
from django.http import JsonResponse
import json

from django.urls import reverse

#Admin Only Product
from .forms import ProductForm

def is_admin(user):
    return user.is_staff

from django.contrib.auth.decorators import login_required, user_passes_test

import logging
logger = logging.getLogger(__name__)
@login_required
def product_list(request):
    products = Product.objects.all()
    for product in products:
        logger.debug(f"Product Image: {product.img.url}")
    return render(request, 'orders/product_list_crud.html', {'products': products})


def product_setting(request):
    # Handle form submission
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_setting')
    else:
        form = ProductForm()

    # Get all products
    products = Product.objects.all()

    # Create a list of products with their stock values directly from the Product model
    products_with_stock = []
    for product in products:
        # Get stock from the Product model
        stock = product.stock  # Get the stock value from the model directly
        products_with_stock.append({'product': product, 'stock': stock})

    # Pass both form and product information to the template
    return render(request, 'orders/product_setting.html', {'form': form, 'products_with_stock': products_with_stock})

# Update Stock Product

@user_passes_test(is_admin)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Produk berhasil ditambahkan!")
            return redirect('product_list')
        else:
            messages.error(request, "Gagal menambahkan produk. Periksa form.")
    else:
        form = ProductForm()
    return render(request, 'orders/product_form.html', {'form': form})

def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect ke daftar produk setelah berhasil menambah
    else:
        form = ProductForm()
    return render(request, 'orders/product_add.html', {'form': form})

def product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect ke daftar produk setelah berhasil mengedit
    else:
        form = ProductForm(instance=product)
    return render(request, 'orders/product_edit.html', {'form': form, 'product': product})




from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Product

@user_passes_test(is_admin)
def update_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        if 'increase' in request.POST:
            product.stock += 1  # Increase stock by 1
        elif 'decrease' in request.POST:
            if product.stock > 0:
                product.stock -= 1  # Decrease stock by 1 if stock is greater than 0
            else:
                error_message = "Stock cannot be negative."
                return render(request, 'orders/update_stock.html', {'product': product, 'error_message': error_message})

        product.save()
        return HttpResponseRedirect(reverse('product_summary', args=[product.pk]))  # Redirect back to product summary page

    return render(request, 'orders/update_stock.html', {'product': product})
# Stock
from django.db.models import Q

def product_summary(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'orders/product_summary.html', {'product': product})

@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Produk berhasil dihapus.")
        return redirect('product_list')
    return render(request, 'orders/product_confirm_delete.html', {'product': product})


# Checkout
@login_required
def checkout(request):
    if request.method == 'POST':
        # Simpan data pesanan
        user = request.user
        items = request.session.get('cart', {})  # Ambil data dari session (contoh keranjang belanja)
        if not items:
            messages.error(request, 'Your cart is empty.')
            return redirect('cart')

        order = Order.objects.create(user=user, status='Pending')
        total_price = 0

        for product_id, quantity in items.items():
            product = get_object_or_404(Product, id=product_id)
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )
            total_price += product.price * quantity

            # Update stok produk
            product.stock -= quantity
            product.save()

        order.total_price = total_price
        order.save()

        # Hapus keranjang setelah checkout
        del request.session['cart']

        messages.success(request, 'Your order has been placed successfully.')
        return redirect('order_history')

    return render(request, 'orders/checkout.html')
# Checkout

# History



# Order Detail
from django.shortcuts import render, get_object_or_404
from .models import Order


@login_required
def order_detail(request, order_id):
    try:
        # Ambil detail pesanan berdasarkan ID
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)

        # Kirim data ke template untuk ditampilkan
        return render(request, 'orders/order_detail.html', {
            'order': order,
            'order_items': order_items,
        })
    except Order.DoesNotExist:
        return render(request, '404.html', {'message': 'Order not found'}, status=404)

def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})


# Alur dari payment_order ke user_order_views
@login_required
def user_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Fetch orders for the logged-in user
    return render(request, 'orders/orders.html', {'orders': orders})
# Alur End

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'orders/product_list.html', {'products': products})

# Order List
@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})
# Order List End

# Home Start
def home(request):
    try:
        order = get_object_or_404(Order, user=request.user)  # Adjust as necessary
        print(f"Order ID: {order.id}")  # Debugging line
    except Exception as e:
        print(f"Error: {e}")  # Print any errors
        order = None  # Set order to None if there's an error
    return render(request, 'home.html', {'order': order})


# Home End
