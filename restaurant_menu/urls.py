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
    path('profile/', views.profile, name="profile"),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('place_order/', views.place_order, name='place_order'),
    path('forgot-password/', views.forgot_password, name="forgot_password"),
    path('forgot-password/done/', views.send_reset_email, name="send_reset_email"),
    path('reset-password/<uidb64>/<token>/', views.confirm_reset_password, name="confirm_reset_password"),
    path('reset-password/done/', views.reset_password_completed, name="reset_password_completed"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
