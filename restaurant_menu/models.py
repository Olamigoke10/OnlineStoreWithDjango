from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

MEAL_TYPE = (
    ("starters", "Starters"),
    ("salads", "Salads"),
    ("main_dishes", "Main Dishes"),
    ("desserts", "Desserts"),
)

STATUS = (
    (0, "Unavailable"),
    (1, "Available"),
)

ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Item(models.Model):
    meal = models.CharField(max_length=1000, unique=True)
    description = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    meal_type = models.CharField(max_length=200, choices=MEAL_TYPE)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.IntegerField(choices=STATUS, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)  # Add this line

    def __str__(self):
        return self.meal


# New Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Indicates if the cart is still active (e.g., not checked out)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

    def get_total_price(self):
        total = sum(item.get_total_price() for item in self.cartitem_set.all())
        return total


# New CartItem Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        unique_together = ('cart', 'item')

    def __str__(self):
        return f"{self.quantity} of {self.item.meal} in cart {self.cart.id}"

    def get_total_price(self):
        return self.item.price * self.quantity
    
    
class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.item} by {self.user.username}'
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='Pending')
    estimated_delivery = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
    def update_status(self):
        now = timezone.now()
        time_since_creation = now - self.created_at

        if self.status == 'Pending':
            if time_since_creation >= timezone.timedelta(minutes=1):  # Example: Change to 'Confirmed' after 1 minute for testing
                self.status = 'Confirmed'
                self.save()
        elif self.status == 'Confirmed':
            if time_since_creation >= timezone.timedelta(minutes=2):  # Example: Change to 'Delivered' after 2 minutes for testing
                self.status = 'Delivered'
                self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.item.meal}"
    

def default_video_file_path():
    # Example logic to generate a default file path
    return 'videos/default_video.mp4'
    
    
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/', default=default_video_file_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
