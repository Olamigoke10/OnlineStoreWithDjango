from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, MEAL_TYPE, Cart, CartItem, Profile, Order, OrderItem
from .forms import SignUpForm, LoginForm, ProfileUpdateForm, UserUpdateForm, ReviewForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from functools import wraps
from django.http import JsonResponse


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
    reviews = item.reviews.all()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()
            return redirect('menu_item_detail', pk=item.pk)
    else:
        review_form = ReviewForm()

    return render(request, 'base/menu_item_detail.html', {
        'object': item,
        'reviews': reviews,
        'review_form': review_form
    })


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(first_name=first_name, last_name=last_name, username=username, password=raw_password)
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
            
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user)
            
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
        
        # Calculate the updated total price for the item and the entire cart
        item_total = cart_item.get_total_price() if quantity > 0 else 0
        total_price = cart.get_total_price()  # Assuming you have this method

        return JsonResponse({
            'item_total': item_total,
            'total_price': total_price
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)



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
    cart = get_user_cart(request.user)  # Replace with your logic to get user's cart

    try:
        cart_item = CartItem.objects.get(cart=cart, item=item)
    except CartItem.DoesNotExist:
        raise Http404("Cart item not found")
    except CartItem.MultipleObjectsReturned:
        # Handle the case where multiple CartItems are found (should not happen ideally)
        # Log an error or choose which one to delete
        # For simplicity, you can delete all instances found
        CartItem.objects.filter(cart=cart, item=item).delete()
        return redirect('view_cart')

    # Delete the single CartItem found
    cart_item.delete()
    return redirect('view_cart')



# User_profile
@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
            
    context = {
        'user': request.user,
        'u_form': u_form,
        'p_form': p_form
    }
        
    return render(request, 'base/profile.html', context)


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after successful update
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'base/profile_update.html', {'form': form})



@login_required
def add_review(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()
            return redirect('menu_item_detail', pk=item_id)
    else:
        form = ReviewForm()
    
    return render(request, 'base/add_review.html', {'form':form, 'item':item})    



def place_order(request):
    if request.method == "POST":
        user = request.user
        cart = get_object_or_404(Cart, user=user, is_active=True)
        if not cart.cartitem_set.exists():
            return JsonResponse({'error': 'Cart is empty'}, status=400)

        # Create order
        order = Order.objects.create(user=user, total_price=cart.get_total_price())

        # Add items to order
        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
                price=cart_item.item.price
            )

        # Clear the cart
        cart.cartitem_set.all().delete()
        cart.is_active = False
        cart.save()

        return JsonResponse({'success': 'Order placed successfully', 'order_id': order.id})

    return redirect('cart')  
    