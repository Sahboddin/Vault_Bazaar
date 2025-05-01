from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from cart.models import Cart, CartItem
from orders.models import Product,Payment,Order,OrderProduct

from cart.views import merge_cart_items
from django.core.exceptions import ObjectDoesNotExist

def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cart')
    return render(request, 'accounts/register.html', {'form':form})

def profile(request):
    
    # total = 0
    # grand_total = 0
    # quantity = 0
    # delivary_charge = 0
    # final_total = 0
    # cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    # for cart_item in cart_items:
    #     total += (cart_item.product.price * cart_item.quantity)
    #     quantity += cart_item.quantity
    # tax = (2 * total)/100
    # grand_total = total + tax
    # delivary_charge = quantity * 20
    # final_total = grand_total + delivary_charge
    

    # context = {
        # 'total': total,
        # 'quantity': quantity,
        # 'cart_items': cart_items,
        # 'delivary_charge'       : delivary_charge,
        # 'grand_total': grand_total,
        # 'final_total': final_total,
    # }
    order = Order.objects.filter(user=request.user).order_by('-order_number').first()
    order_product = OrderProduct.objects.filter(order=order)
    # delivary_charge = 100
    sub_total = 0
    quantity = 0
    if order:
        for product in order_product:
            sub_total += product.product.price * product.quantity
        
        
        final_total = order.order_total
        tax = order.tax
        
        context = {
            "sub_total": sub_total,
            "order" : order,
            'order_items': order_product,
            # 'delivary_charge'  : delivary_charge,
            'final_total': final_total,
            'tax': tax,
        }
        return render(request, 'accounts/dashboard.html',context)
    
    return render(request, 'accounts/dashboard.html')
    
    

# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username = user_name, password = password)
#         print(user)
#         # ekhono login hoy nai
#         session_key = get_create_session(request)
        
#         # cart = Cart.objects.get(cart_id = session_key)
        
#         cart, created = Cart.objects.get_or_create(cart_id=session_key)
#         is_cart_item_exists = CartItem.objects.filter(cart = cart).exists()
#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(cart = cart)
#             for item in cart_item:
#                 item.user = user
#                 item.save()
#         login(request, user)
        
#         # login hoye geche
        
#         return redirect('profile')
#     return render(request, 'accounts/signin.html')

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=user_name, password=password)

        if user is not None:
            # Before login, get or create session key
            session_key = get_create_session(request)
            
            # Get or create a Cart using the session key
            cart, created = Cart.objects.get_or_create(cart_id=session_key)
            
            # Check if there are any items in the session cart
            if CartItem.objects.filter(cart=cart).exists():
                cart_items = CartItem.objects.filter(cart=cart)

                # Transfer session cart items to the logged-in user
                for item in cart_items:
                    item.user = user
                    item.cart = None  # Clear session cart reference
                    item.save()

            # Now log the user in
            login(request, user)
            
            # After login, merge any duplicate cart items for the user
            merge_cart_items(user)  # Merge cart items after login
            
            return redirect('profile')

    return render(request, 'accounts/signin.html')




def user_logout(request):
    logout(request)
    return redirect('login')


