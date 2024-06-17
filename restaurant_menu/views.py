from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, MEAL_TYPE, Cart, CartItem
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from functools import wraps


def user_not_registered_redirect(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('register')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def menu_list(request):
    meals = MEAL_TYPE
    items = Item.objects.order_by('-date_created')
    return render(request, 'base/home.html', {'meals': meals, 'object_list': items})

def menu_item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'base/menu_item_detail.html', {'object': item})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'base/signup.html', {'form':form})

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        user = authenticate(request, username=username, password=password)
            
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('home')
        else:
            messages.error(request, "Username does not exist")
        
    return render(request, 'base/signup.html', {'page':page})

def logoutUser(request):
    logout(request)
    return redirect('home')

def contactUs(request):
    return render(request, 'base/contact.html')


@user_not_registered_redirect
@login_required
def add_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Get or create the cart
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    
    # Check if item is already in cart
    cart_item,created = CartItem.objects.get_or_create(cart=cart, item=item)
    
    if not created:
        # Item is already in the cart, so we update the quantity
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('view_cart')


@user_not_registered_redirect
@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user, is_active=True).first()
    cart_items = CartItem.objects.filter(cart=cart)
    
    total_price = sum(item.get_total_price() for item in cart_items)  
    
    context = {
        'cart': cart,
        'cart_items':cart_items,
        'total_price':total_price
    }  
    
    return render(request, 'base/cart.html', context)


@user_not_registered_redirect
@login_required
def update_cart_item(request, item_id):
    cart = Cart.objects.filter(user=request.user, is_active=True).first()
    item = get_object_or_404(Item, id=item_id)
    cart_item = get_object_or_404(CartItem, cart=cart, item=item)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
            
    return redirect('view_cart')



from django.http import Http404

def get_user_cart(user):
    try:
        return Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        raise Http404("Cart does not exist")



@user_not_registered_redirect
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = get_user_cart(request.user)  # This is a hypothetical function to get the user's cart.

    # Assuming cart and item should uniquely identify a CartItem
    cart_item = CartItem.objects.filter(cart=cart, item=item).first()

    if not cart_item:
        # Handle case where no cart item is found
        raise Http404("Cart item not found")

    # Proceed with removing the item from the cart
    cart_item.delete()
    return redirect('view_cart')

