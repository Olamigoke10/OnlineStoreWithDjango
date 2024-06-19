from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, MEAL_TYPE, Cart, CartItem, Profile, Order, OrderItem, ORDER_STATUS, Video
from .forms import SignUpForm, LoginForm, ProfileUpdateForm, UserUpdateForm, ReviewForm, ContactForm, OrderFilterForm , VideoForm, FeedbackForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from functools import wraps
from django.http import JsonResponse
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings



def is_admin(user):
    return user.is_authenticated and user.is_staff


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
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # Send email to the user
            subject = 'Welcome to Our Site'
            message = f'Hi {first_name} {last_name}, thank you for registering on our site.'
            from_email = settings.EMAIL_HOST_USER  # Use your own email settings from settings.py
            to_email = [user.email]  # Assuming user.email is where you store the user's email

            try:
                send_mail(subject, message, from_email, to_email, fail_silently=False)
                messages.success(request, 'Registration successful. Welcome to our site!')
            except Exception as e:
                messages.warning(request, f'Failed to send registration email. Error: {e}')

            return redirect('home')  # Redirect to home after successful registration
    else:
        form = SignUpForm()

    return render(request, 'base/signup.html', {'form': form})

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

def aboutUs(request):
    return render(request, 'base/about.html')


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
        
    return redirect('home')


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
        total_price = cart.get_total_price() 

        return JsonResponse({
            'item_total': item_total,
            'total_price': total_price
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)



from django.http import Http404

def get_user_cart(user):
    try:
        return Cart.objects.get(user=user, is_active=True)
    except Cart.DoesNotExist:
        raise Http404("Cart does not exist")



@user_not_registered_redirect
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = get_user_cart(request.user)  

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

        # Calculate estimated delivery time
        estimated_delivery = datetime.now() + timedelta(minutes=30)  # Assuming 30 minutes delivery time

        # Create order
        order = Order.objects.create(
            user=user, 
            total_price=cart.get_total_price(),
            status='Pending',  # Initial status set to Pending
            estimated_delivery=estimated_delivery
        )

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

        # Create a new empty cart for the user
        Cart.objects.create(user=user, is_active=True)

        return JsonResponse({
            'success': 'Order placed successfully',
            'order_id': order.id,
            'estimated_delivery': order.estimated_delivery.strftime('%Y-%m-%d %H:%M:%S')  # Formatting for JSON response
        })

    
    
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'base/order_history.html', {'orders': orders})


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'base/order_details.html', {'order': order})

    
    
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']

            # Optionally, send an email or save data to the database
            # For now, let's just print it to the console
            print(f"Received contact form: {first_name} {last_name}, Email: {email}, Subject: {subject}")

            # Redirect to a 'thank you' page or the same page with a success message
            return redirect('thank_you')  # Replace with your URL name or path

    else:
        form = ContactForm()

    return render(request, 'contact', {'form': form})



def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Get the form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']

            # Send feedback response email
            send_mail(
                'Thank you for your feedback',
                'Dear {},\n\nThank you for your feedback! We appreciate you taking the time to reach out to us.\n\nBest Regards,\nR-Foods Team'.format(first_name),
                settings.EMAIL_HOST_USER,  # This is the sender email
                [email],  # This is the recipient email
                fail_silently=False,
            )

            return redirect('feedback_thanks')  # Redirect to a thank you page
    else:
        form = FeedbackForm()
    
    return render(request, 'base/contact.html', {'form': form})



# Resturant Owners

@login_required
@user_passes_test(is_admin)
def orders_view(request):
    # Fetch all orders for today
    today = timezone.now().date()
    orders = Order.objects.filter(created_at__date=today)
    
    # Handle status filter if provided
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Update order statuses based on time criteria (every 60 seconds)
    for order in orders:
        if order.status == 'Pending' and timezone.now() - order.created_at >= timezone.timedelta(seconds=60):
            order.status = 'Confirmed'
            order.save()
        elif order.status == 'Confirmed' and timezone.now() - order.created_at >= timezone.timedelta(seconds=120):
            order.status = 'Delivered'
            order.save()
    
    # Prepare context for rendering template
    context = {
        'orders': orders,
        'status_choices': ORDER_STATUS,
        'selected_status': status_filter
    }
    
    return render(request, 'base/order_list.html', context)
    
    
@user_passes_test(is_admin)
def video_list(request):
    videos = Video.objects.all()
    return render(request, 'base/video_list.html', {'videos': videos})

def add_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video_list')  # Redirect to video list page
    else:
        form = VideoForm()
    return render(request, 'base/add_video.html', {'form': form})

def edit_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('video_list')  # Redirect to video list page
    else:
        form = VideoForm(instance=video)
    return render(request, 'base/edit_video.html', {'form': form, 'video': video})