from django.shortcuts import render
# Import models from various apps
from store.models import Product, ReviewRating
from category.models import Category
from cart.models import Cart, CartItem
from orders.models import Payment, Order, OrderProduct, PaymentGateWaySettings

def home(request):
    """
    Home view:
    Renders the main landing page of the website (index.html).
    Does not supply any additional context data.
    """
    return render(request, 'index.html')


def global_context(request):
    """
    Global context processor:
    Gathers site-wide data and makes it available in all templates.

    Variables provided:
    - products: All Product instances (e.g., for featured lists or searches).
    - categories: All Category instances (e.g., for navigation menus).
    - carts: All Cart instances (not filtered by user; consider limiting scope).
    - cart_items: All CartItem instances (ditto).
    - review_ratings: All ReviewRating instances (e.g., for displaying latest reviews).
    - payments: All Payment instances (e.g., admin dashboards).
    - orders: All Order instances (e.g., order history).
    - order_products: All OrderProduct instances (e.g., detailed order views).
    - payments_gateways: All PaymentGateWaySettings instances (e.g., for checkout configurations).

    Note: Loading all records on every request can impact performance. 
    Consider filtering by user, limiting fields, or caching as needed.
    """
    products = Product.objects.all()
    categories = Category.objects.all()
    carts = Cart.objects.all()
    cart_items = CartItem.objects.all()
    review_ratings = ReviewRating.objects.all()
    payments = Payment.objects.all()
    orders = Order.objects.all()
    order_products = OrderProduct.objects.all()
    payments_gateways = PaymentGateWaySettings.objects.all()

    return {
        'products': products,
        'categories': categories,
        'carts': carts,
        'cart_items': cart_items,
        'review_ratings': review_ratings,
        'payments': payments,
        'orders': orders,
        'order_products': order_products,
        'payments_gateways': payments_gateways,
    }
