from functools import wraps
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import *
from .forms import *


def vip_customer_check(view_function=None):
    @wraps(view_function)
    def _wrapped_view(request, *args, **kwargs):
        request.has_passed_vip_check = False

        if request.method == 'POST':
            form = AddNewOrderForm(request.POST)
            if form.is_valid():
                customer_is_vip = form.cleaned_data['customer_is_vip']
                product_id = form.cleaned_data['product_id']
                product_requires_vip = Product.objects.all().get(product_id=product_id).vip
                if product_requires_vip:
                    if customer_is_vip:
                        request.has_passed_vip_check = True
                    else:
                        messages.error(request, 'Must be VIP')
                else:
                    request.has_passed_vip_check = True
        return view_function(request, *args, **kwargs)
    return _wrapped_view


def stock_pcs_enough_check(view_function=None):
    @wraps(view_function)
    def _wrapped_view(request, *args, **kwargs):
        request.is_stock_pcs_enough = False

        if request.method == 'POST':
            form = AddNewOrderForm(request.POST)
            if form.is_valid():
                product_id = form.cleaned_data['product_id']
                qty = form.cleaned_data['qty']
                stock_pcs = Product.objects.all().get(product_id=product_id).stock_pcs
                if stock_pcs >= qty:
                    request.is_stock_pcs_enough = True
                else:
                    messages.error(
                        request, 'Not enough product qty in stock!')
        return view_function(request, *args, **kwargs)
    return _wrapped_view


@vip_customer_check
@stock_pcs_enough_check
@require_POST
def add_order(request):
    form = AddNewOrderForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        product_id = form.cleaned_data['product_id']
        customer_id = form.cleaned_data['customer_id']
        qty = form.cleaned_data['qty']

        if request.is_stock_pcs_enough and request.has_passed_vip_check:
            try:
                product = Product.objects.all().get(product_id=product_id)
                customer = Customer.objects.all().get(customer_id=customer_id)
                order_data = {
                    'product_id': product,
                    'qty': qty,
                    'price': product.price * qty,
                    'shop_id': product.shop_id,
                    'customer_id': customer,
                }
                order = Order.objects.create(**order_data)
                print(order)
                product.stock_pcs -= qty
                product.save()
                messages.info(request, 'Added a new order!')
            except:
                messages.error(request, 'Failed to add order!')
        else:
            messages.error(request, 'Failed to add order!')
    else:
        messages.error(request, 'Invalid form!')

    return redirect('index')


@require_POST
def remove_order(request):
    try:
        order_id = int(request.POST.get('order_id'))
        order = Order.objects.all().get(order_id=order_id)
        product = order.product_id
        if product.stock_pcs == 0:
            messages.info(
                request, f'Product {product.product_id} in stock now!')
        product.stock_pcs += order.qty
        product.save()
        messages.info(request, f'Order {order.order_id} removed!')
        order.delete()
    except:
        messages.error(request, 'ERROR occurred while removing order')
        raise
    return redirect('index')


def index(request):
    products = Product.objects.all()
    orders = Order.objects.all()
    form = AddNewOrderForm()
    context = {
        'products': products,
        'orders': orders,
        'form': form,
    }
    return render(request, 'index.html', context)
