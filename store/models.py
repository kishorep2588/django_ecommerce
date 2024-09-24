from django.db import models
import datetime 
import uuid

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0) ## 9999.99
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    ## Adding Sale Details
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)


    def __str__(self):
        return self.name
    
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)    ## (341)-(3000)-(675)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Order(models.Model):
    catogery = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.datetime.today)
    order_id = models.IntegerField(default=uuid.uuid4())

    def __str__(self):
        return str(self.order_id)


