from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, MEAL_TYPE
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages

def menu_list(request):
    meals = MEAL_TYPE
    items = Item.objects.order_by('-date_created')
    return render(request, 'base/index.html', {'meals': meals, 'object_list': items})

def menu_item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'base/menu_item_detail.html', {'object': item})


def register(request):
    if request.method == 'POST':
        form =SignUpForm(request.POST)
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


