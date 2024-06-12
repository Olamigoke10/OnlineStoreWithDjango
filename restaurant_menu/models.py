from django.db import models
from django.contrib.auth.models import User

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

class Item(models.Model):
    meal = models.CharField(max_length=1000, unique=True)
    description = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    meal_type = models.CharField(max_length=200, choices=MEAL_TYPE)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.IntegerField(choices=STATUS, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


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

    def __str__(self):
        return f"{self.quantity} of {self.item.meal} in cart {self.cart.id}"

    def get_total_price(self):
        return self.item.price * self.quantity