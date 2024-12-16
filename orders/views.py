from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from Payment.models import Payment
from django.contrib.auth.decorators import login_required
from halaman.models import UserProfile
# from orders.models import Product
from django.db import transaction
from django.http import HttpResponseBadRequest

# from .models import Order, OrderItem, Product
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


@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Produk berhasil dihapus.")
        return redirect('product_list')
    return render(request, 'orders/product_confirm_delete.html', {'product': product})

# History



# Order Detail
from django.shortcuts import render, get_object_or_404
# from .models import Order


# @login_required
# def order_detail(request, order_id):
#     try:
#         # Ambil detail pesanan berdasarkan ID
#         order = Order.objects.get(id=order_id, user=request.user)
#         order_items = OrderItem.objects.filter(order=order)

#         # Kirim data ke template untuk ditampilkan
#         return render(request, 'orders/order_detail.html', {
#             'order': order,
#             'order_items': order_items,
#         })
#     except Order.DoesNotExist:
#         return render(request, '404.html', {'message': 'Order not found'}, status=404)

# def order_detail_view(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return render(request, 'orders/order_detail.html', {'order': order})


# Alur dari payment_order ke user_order_views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from .models import Order

# @login_required
# def user_orders_view(request):
#     orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Fetch orders for the logged-in user
    
#     for order in orders:
#         # Check if the order has an associated payment and update the payment status
#         if order.payments.exists():  # If payments exist for this order
#             payment = order.payments.first()  # Get the most recent payment
#             order.payment_status = payment.status
#         else:
#             order.payment_status = 'Pending'  # If no payment exists

#     return render(request, 'orders/orders.html', {'orders': orders})

# Alur End
def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'orders/product_list.html', {'products': products})

# Order List
# @login_required
# def order_list_view(request):
#     orders = Order.objects.filter(user=request.user)
#     return render(request, 'orders/order_list.html', {'orders': orders})
# # Order List End

# Home Start
@login_required
def home(request):
    return render(request, 'home.html', {
        'user': request.user,
    })


logger = logging.getLogger(__name__)
# Create your views here.
def home(request):
    logger.info("Home view accessed")
    return render(request, 'home.html')

# Home End

# Profile 
from halaman.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Product
def profilePage(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to view your profile.")
        return redirect('login')

    # Ambil profil pengguna yang sedang login (dari UserProfile)
    profile = UserProfile.objects.filter(user=request.user).first()

    context = {
        'user': request.user,
        'profile': profile  # Tambahkan profil pengguna ke context
    }
    return render(request, 'accounts/profile.html', context)

def logoutUser(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')



def product_list(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'orders/product_list_crud.html', {'products': products})