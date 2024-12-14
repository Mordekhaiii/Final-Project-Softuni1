from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment, Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction
from .forms import PaymentForm  # Impor PaymentForm
from .models import Product, Payment
from orders.models import Order


@login_required
def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    try:
        with transaction.atomic():

            product = payment.product
            product.stock += payment.quantity
            product.is_available = True
            product.save()

            payment.delete()

    except Exception as e:
        pass

    return redirect('payment_list')


@login_required
def decrease_quantity(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    try:
        with transaction.atomic():
            if payment.quantity > 1:
                payment.quantity -= 1
                payment.total_price = payment.quantity * payment.product.price
                payment.save()

                perfume = payment.product
                perfume.stock += 1
                perfume.is_available = True
                perfume.save()

    except Exception as e:
        pass

    return redirect('payment_list')




from django.contrib import messages

@login_required
def payment_list(request):
    product_id = request.GET.get('product_id')
    quantity = int(request.GET.get('quantity', 1))

    if product_id:
        try:
            # Get the product by ID
            product = get_object_or_404(Product, id=product_id)

            # Ensure a pending order exists for the user
            order, created = Order.objects.get_or_create(user=request.user, status='pending')

            # Check if the product is already in the order
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
                defaults={'quantity': quantity, 'price': product.price}
            )
            if not created:
                # Update the quantity for an existing item
                if product.stock >= quantity:
                    order_item.quantity += quantity
                    order_item.save()
                else:
                    messages.error(request, "Insufficient stock for this product.")
                    return redirect('product_list')

            # Deduct the product stock
            if product.stock >= quantity:
                product.stock -= quantity
                product.save()
            else:
                messages.error(request, "Insufficient stock for this product.")
                return redirect('product_list')

        except Exception as e:
            messages.error(request, f"Error adding product: {e}")
            return redirect('product_list')

    # Fetch all items in the current pending order
    payments = OrderItem.objects.filter(order__user=request.user, order__status='pending')
    total_payment = sum(item.quantity * item.price for item in payments)

    return render(request, 'payment/payment_list.html', {'payments': payments, 'total_payment': total_payment})


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from orders.models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required

@login_required
def payment_order(request, order_id):
    try:
        # Get the product from the database
        product = get_object_or_404(Product, id=order_id)

        # Ensure only one pending order exists for the user
        orders = Order.objects.filter(user=request.user, status='pending')
        if orders.exists():
            order = orders.first()  # Get the first order if multiple exist
            if orders.count() > 1:
                # Remove duplicates and keep only one
                orders.exclude(id=order.id).delete()
        else:
            # Create a new order if none exists
            order = Order.objects.create(user=request.user, status='pending')

        # Get the quantity from the query parameters (default to 1)
        quantity = int(request.GET.get('quantity', 1))

        # Check stock availability
        if product.stock < quantity:
            return JsonResponse({
                'status': 'error',
                'message': 'Not enough stock available'
            }, status=400)

        # Check if the product is already in the order
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'quantity': quantity, 'price': product.price}
        )
        if not created:
            # If it already exists, update the quantity
            order_item.quantity += quantity
            order_item.save()

        # Update the product stock
        product.stock -= quantity
        product.save()

        # Redirect to the payment page
        return redirect('payment_order', product_id=product.id)  # Ganti 'payment:checkout' dengan nama URL Anda

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error adding product to order: {str(e)}'
        }, status=500)

