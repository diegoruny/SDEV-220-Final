from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, Customer
from django.contrib.auth.decorators import login_required

# Create your views here.

def product_list(request):
    """Display a list of available coffee products."""
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, product_id):
    """Display product details."""
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    """Add a product to the shopping cart."""
    product = get_object_or_404(Product, id=product_id)
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1
    order_item.save()
    return redirect('shop:cart')

@login_required
def remove_from_cart(request, product_id):
    """Take all instances of a product out of the shopping cart."""
    #product = get_object_or_404(Product, id=product_id)
    customer, created = Customer.objects.get(user=request.user)
    order, created = Order.objects.get(customer=customer)
    items = OrderItem.objects.get(order=order)
    if product_id in items:
        item = OrderItem.objects.get(product=product_id)
        item.objects.delete() # remove the item
    return redirect('shop:cart')

@login_required
def cart(request):
    """Display the shopping cart."""
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    context = {'items': items, 'order': order}
    return render(request, 'shop/cart.html', context)

@login_required
def checkout(request):
    """Handle the checkout process."""
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # Implement payment processing logic here
    # For now, we'll set the order as complete
    if request.method == 'POST':
        order.reward_points() # add points to user account
        order.complete = True
        order.save()
        return redirect('shop:product_list')
    context = {'order': order}
    return render(request, 'shop/checkout.html', context)

@login_required
def cancel_order(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order.objects.delete()
    return render(request,'shop/product_list.html')