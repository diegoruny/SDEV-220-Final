from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, Customer
from django.contrib.auth.decorators import login_required

# Create your views here.

def product_list(request):
    """Display a list of available coffee products."""
    customer, created = Customer.objects.get_or_create(user=request.user)
    points = customer.return_points
    products = Product.objects.all()
    context = {'products': products,'user' : customer, 'points' : points}
    return render(request, 'shop/product_list.html', context = context)

def product_detail(request, product_id):
    """Display product details."""
    customer, created = Customer.objects.get_or_create(user=request.user)
    points = customer.return_points
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product,'user' : customer, 'points' : points}
    return render(request, 'shop/product_detail.html', context = context)

@login_required
def add_to_cart(request, product_id):
    """Add a product to the shopping cart."""
    product = get_object_or_404(Product, id=product_id)
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1
    order_item.save()
    return redirect('shop:product_list')
    # return redirect('shop:cart') Allow users to stay on the product list without having to go the cart

@login_required
def cart(request):
    """Display the shopping cart."""
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    points = customer.return_points
    items = order.orderitem_set.all()
    context = {'items': items, 'order': order, 'points' : points}
    return render(request, 'shop/cart.html', context)

@login_required
def checkout(request):
    """Handle the checkout process."""
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    points = customer.return_points
    # Implement payment processing logic here
    # For now, we'll set the order as complete
    if request.method == 'POST':
        order.reward_points() # add points to user account
        order.complete = True
        order.save()
        return redirect('shop:product_list')
    context = {'order': order, 'points' : points}
    return render(request, 'shop/checkout.html', context)

@login_required
def clear_cart(request):
    """Remove all products from cart."""
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    for item in OrderItem.objects.filter(order=order):
        print('Removed',item)
        item.delete()
    return redirect('shop:cart')

@login_required
def cancel_order(request):
    """Destroy an order object"""
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order.delete()
    return redirect('shop:product_list')