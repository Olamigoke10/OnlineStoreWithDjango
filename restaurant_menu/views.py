from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, MEAL_TYPE, Cart, CartItem, Profile, Order, OrderItem
from .forms import SignUpForm, LoginForm, ProfileUpdateForm, UserUpdateForm, ReviewForm, ContactForm, ForgotPasswordForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from functools import wraps
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.conf import settings


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
            user = authenticate(first_name=first_name, last_name=last_name,
                                username=username, password=raw_password)
            login(request, user)
            return redirect('home')
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

    return render(request, 'base/signup.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('home')


def forgot_password(request):
    if request.method == "POST":
        forgot_password_form = ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            data = forgot_password_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "base/forgot_password_email.html"
                    c = {
                        "email": user.email,
                        'domain': request.get_host(),
                        'site_name': 'Feane',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_content = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email_content, settings.DEFAULT_FROM_EMAIL, [
                                  user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("send_reset_email")
    forgot_password_form = ForgotPasswordForm()
    return render(request, "base/forgot_password.html", {"forgot_password_form": forgot_password_form})


def send_reset_email(request):
    return render(request, "base/reset_email_sent.html")


def confirm_reset_password(request, uidb64=None, token=None):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        validlink = True
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect("reset_password_completed")
        else:
            form = SetPasswordForm(user)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    return render(request, "base/confirm_reset_password.html", context)


def reset_password_completed(request):
    return render(request, "base/reset_password_completed.html")


def contactUs(request):
    return render(request, 'base/contact.html')


@user_not_registered_redirect
@login_required
def add_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    # Get or create the cart
    cart, created = Cart.objects.get_or_create(
        user=request.user, is_active=True)

    # Check if item is already in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

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
        'cart_items': cart_items,
        'total_price': total_price
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


def get_user_cart(user):
    try:
        return Cart.objects.get(user=user, is_active=True)
    except Cart.DoesNotExist:
        raise Http404("Cart does not exist")



@user_not_registered_redirect
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    # Use the new function to get user's cart
    cart = get_user_cart(request.user)

    try:
        cart_item = CartItem.objects.get(cart=cart, item=item)
    except CartItem.DoesNotExist:
        raise Http404("Cart item not found")
    except CartItem.MultipleObjectsReturned:
        # Delete all instances found for this item in the cart
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
            # Redirect to profile page after successful update
            return redirect('profile')
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

    return render(request, 'base/add_review.html', {'form': form, 'item': item})


def place_order(request):
    if request.method == "POST":
        user = request.user
        cart = get_object_or_404(Cart, user=user, is_active=True)
        if not cart.cartitem_set.exists():
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        
        estimated_delivery = datetime.now() + timedelta(hours=1) 

        # Calculate total price
        total_price = cart.get_total_price()

        # Create the order
        order = Order.objects.create(
            user=user, 
            total_price=total_price,
            status='Pending',  # Initial status
            estimated_delivery= estimated_delivery  
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

        return JsonResponse({'success': 'Order placed successfully', 'order_id': order.id})
    
    
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
    
