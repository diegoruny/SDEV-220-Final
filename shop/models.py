from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import decimal

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields (optional)
    address = models.CharField(max_length=255, null=True, blank=True)
    reward_points = models.IntegerField(default=0,null=True,blank=True)

    @property
    def return_points(self):
        return self.reward_points

    def __str__(self):
        return self.user.username
    
    def add_points(self,amount):
        self.reward_points += amount
        self.save()

    def deduct_points(self,amount):
        self.reward_points -= amount
        self.save()
    
class Product(models.Model):
    """Model representing a coffee product."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    point_value = models.IntegerField(default=25,blank=True,null=True) # Number of points awarded per purchase

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    reward_applied = models.BooleanField(default=False)

    @property
    def get_cart_subtotal(self):
        orderitems = self.orderitem_set.all()
        return round(sum([item.get_total for item in orderitems]),2)
    
    @property
    def get_tax_amount(self):
        tax_rate = decimal.Decimal(0.08) # 8% tax rate
        orderitems = self.orderitem_set.all()

        if self.reward_applied == True:
            discount = self.get_reward_discount
        else: 
            discount = decimal.Decimal(0.00)

        subtotal = round(sum([item.get_total for item in orderitems]),2) - discount
        return round(tax_rate * subtotal,2)
    
    @property
    def get_reward_discount(self):
        """Apply a discount equal to the price of the highest item"""
        highest_price = decimal.Decimal(0.00)
        discount = decimal.Decimal(0.00) 

        for item in OrderItem.objects.filter(order=self):
            item_product = item.get_product
            if item_product.price > highest_price:
                highest_price = item_product.price
                discount = highest_price
        return discount
    
    @property
    def get_cart_total(self):
        tax_rate = decimal.Decimal(0.08)
        orderitems = self.orderitem_set.all()

        if self.reward_applied == True:
            discount = self.get_reward_discount
        else: 
            discount = decimal.Decimal(0.00)

        subtotal = round(sum([item.get_total for item in orderitems]),2) - discount
        tax_amount = round(subtotal * tax_rate,2)
        
        return (tax_amount + subtotal)
    
    @property
    def get_cart_point_total(self):
        orderitems = self.orderitem_set.all()
        return sum([item.get_points for item in orderitems])
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        return sum([item.quantity for item in orderitems])

    def __str__(self):
        return f"Order {self.id}"
    
    def reward_points(self):
        """Add points to customer account"""
        add_points = self.get_cart_point_total
        account = Customer.objects.get(id=self.customer.id)
        current_points = account.return_points
        new_points = (current_points + add_points)
        account.reward_points=new_points
        account.save()
        return new_points

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        return self.product.price * self.quantity
    
    @property
    def get_points(self):
        return self.product.point_value * self.quantity
    
    @property
    def get_product(self):
        return self.product

    def __str__(self):
        return self.product.name

class CartItem(models.Model):
    """Model representing an item in the shopping cart."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # Add session or user reference

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
