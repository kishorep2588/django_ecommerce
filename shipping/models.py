from django.db import models

from django.contrib.auth.models import User

from store.models import Product

from django.dispatch import receiver
from django.db.models.signals import post_save


class ShippingCategories(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Shipping Categories'


# Create your models here.
class ShippingInfo(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15, blank=True, null=True)
    shipping_category = models.ForeignKey(ShippingCategories, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
    class Meta:
        verbose_name_plural = 'Shipping Info'

class Order(models.Model):
    order_full_name = models.CharField(max_length=100)
    order_email = models.EmailField(max_length=50)
    order_shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'Order - {str(self.id)}'
    
    class Meta:
        verbose_name_plural = 'Order'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f'Order Item - {str(self.id)}'
    
    class Meta:
        verbose_name_plural = 'Order Item'

class UserPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

@receiver(post_save, sender=User)
def create_user_payment(sender, instance, created, **kwargs):
	if created:
		UserPayment.objects.create(user=instance)
