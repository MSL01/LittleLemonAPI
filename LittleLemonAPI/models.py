from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.contrib.auth.models import AbstractUser


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/LittleLemonAPI/images/', default='default.png', max_length=1000)
    def __str__(self):
        return f'{self.user.username} Profile'


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

    def __str__(self)-> str:
        return self.title
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    image = models.ImageField(upload_to='media/LittleLemonAPI/images/', max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1, db_constraint=False)

    def get_price_with_taxes(self):
        return self.price * 1.1


class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems])
        return total

    @property
    def get_cart_items(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total