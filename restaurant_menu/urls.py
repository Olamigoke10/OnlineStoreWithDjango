from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='home'),
    path('item/<int:pk>/', views.menu_item_detail, name='menu_item'),
    path('signup/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
]
