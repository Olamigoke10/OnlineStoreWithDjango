from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.menu_list, name='home'),
    path('item/<int:pk>/', views.menu_item_detail, name='menu_item_detail'),
    path('signup/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name="logout"),
    path('contact/', views.contactUs, name="contact"),
    path('cart/', views.view_cart, name="view_cart"),
    path('cart/add/<int:item_id>/', views.add_cart, name="add_to_cart"),
    path('cart/update/<int:item_id>/', views.update_cart_item, name="update_cart_item"),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('contact/', views.contact_view, name='contact'),
    path('profile/', views.profile, name="profile"),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('place_order/', views.place_order, name='place_order'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_details, name='order_detail'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
