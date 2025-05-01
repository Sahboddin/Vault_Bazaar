from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, user=current_user)
            # print(cart_items)
            item = CartItem.objects.get(product=product, user=current_user)
            item.quantity += 1
            item.save()
    
    
    # if current_user.is_authenticated:
    # # Check if cart items exist for the user and the product
    #     is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        
    #     if is_cart_item_exists:
    #         # Fetch all cart items for the given product and user
    #         cart_items = CartItem.objects.filter(product=product, user=current_user)
            
    #         # Check if there are multiple cart items (i.e., duplicates)
    #         if cart_items.count() > 1:
    #             # Handle duplicates: for example, you might want to combine their quantities
    #             primary_item = cart_items.first()  # Use the first item as the primary one
    #             for duplicate_item in cart_items[1:]:
    #                 # Add the quantity of duplicates to the primary item
    #                 primary_item.quantity += duplicate_item.quantity
    #                 # Delete the duplicate item after merging its quantity
    #                 duplicate_item.delete()
                
    #             # Save the updated primary item
    #             primary_item.save()
    #         else:
    #             # If there's only one item, simply increment its quantity
    #             item = cart_items.first()
    #             item.quantity += 1
    #             item.save()
                
                
        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                )
            cart.save()
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
                user = current_user
            )
            cart_item.save()
        return redirect('cart')
    else:
        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()
        
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity  += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart,
                )
            cart.save()
    return redirect('cart')

def merge_cart_items(user):
    # Fetch all cart items for the logged-in user
    cart_items = CartItem.objects.filter(user=user)

    # Loop through products and merge duplicates
    for product_id in cart_items.values_list('product', flat=True).distinct():
        # Fetch all items for the same product and user
        user_cart_items = CartItem.objects.filter(product_id=product_id, user=user)
        
        if user_cart_items.count() > 1:
            # Merge duplicate cart items
            primary_item = user_cart_items.first()  # First item is primary
            for duplicate_item in user_cart_items[1:]:
                primary_item.quantity += duplicate_item.quantity
                duplicate_item.delete()  # Delete duplicate after merging
            primary_item.save()  # Save updated primary item
            
            
def decrease_cart_item(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    # cart.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        delivary_charge = 0
        cart = None  # Initialize cart to ensure it exists

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        # delivary_charge = quantity * 20
        # grand_total = total + tax + delivary_charge
        grand_total = total + tax
        
    except ObjectDoesNotExist:
        pass #just ignore
    isexist = True
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'delivary_charge' : delivary_charge,
        'grand_total': grand_total,
        'cart' : cart,
        'isexist' : isexist
    }
    return render(request, 'cart/cart.html', context)