from django.shortcuts import render, redirect, HttpResponseRedirect
from cart.models import Cart, CartItem
from .forms import OrderForm
from .models import Payment, OrderProduct, Order
from store.models import Product
from .ssl import sslcommerz_payment_gateway, unique_transaction_id_generator
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from sslcommerz_lib import SSLCOMMERZ
from django.urls import reverse

@csrf_exempt
def success_view(request, tran_id, user_id):
    """
    Handles the success callback after a payment is completed.
    Updates the payment details, order status, and inventory, and clears the cart.
    Redirects to the order completion page.
    """
    data = request.POST
    user = User.objects.get(pk=user_id)
    payment = Payment(
        user=user,
        payment_id=tran_id,
        payment_method=data['card_issuer'],
        amount_paid=int(data['store_amount'][0]),
        status=data['status'],
    )
    payment.save()
    order = Order.objects.get(user=user, is_ordered=False, order_number=data['value_a'])
    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user=user)
    for item in cart_items:
        orderproduct = OrderProduct(
            order=order,
            payment=payment,
            user=user,
            product=item.product,
            quantity=item.quantity,
            ordered=True
        )
        orderproduct.save()
        item.product.stock -= item.quantity
        item.product.save()
    CartItem.objects.filter(user=user).delete()
    return HttpResponseRedirect(reverse('order_complete'))


def order_complete(request):
    """
    Displays the order completion summary including order details, ordered products, and costs.
    """
    order = Order.objects.filter(user=request.user).order_by('-order_number').first()
    order_product = OrderProduct.objects.filter(order=order)
    delivery = 0
    sub_total = sum(product.product.price * product.quantity for product in order_product)
    context = {
        "order": order,
        "order_products": order_product,
        "sub_total": sub_total,
        "delivery": delivery,
    }
    return render(request, 'orders/order_complete.html', context)


def place_order(request):
    """
    Handles the creation of an order and initiates the SSLCommerz payment gateway process.
    Calculates total, tax, and other charges based on cart items.
    """
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        if cart_items.count() < 1:
            return redirect('store')

        total = sum(item.product.price * item.quantity for item in cart_items)
        tax = (2 * total) / 100
        grand_total = total + tax
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.order_total = grand_total
                form.instance.tax = tax
                form.instance.ip = request.META.get('REMOTE_ADDR')
                form.instance.payment = 2
                saved_instance = form.save()
                form.instance.order_number = saved_instance.id
                form.instance.save()
                return redirect(sslcommerz_payment_gateway(request, saved_instance.id, str(request.user.id), grand_total))
        return render(request, 'orders/place-order.html', {'cart_items': cart_items, 'tax': tax, 'total': total, 'grand_total': grand_total})
    else:
        return redirect('login')


def all_order(request):
    """
    Displays all the orders for the logged-in user, including details of each order.
    Redirects to the profile page if no orders exist.
    """
    orders = Order.objects.filter(user=request.user).order_by('-order_number')
    order_product = OrderProduct.objects.filter(user=request.user)
    if orders:
        context = {
            "orders": orders,
            "order_products": order_product,
        }
    else:
        return redirect('profile')
    return render(request, 'orders/all_order.html', context)
