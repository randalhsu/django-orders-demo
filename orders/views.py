from functools import wraps
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
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
                try:
                    product_requires_vip = Product.objects.get(
                        product_id=product_id).vip
                except:
                    messages.error(request, 'Internal error!')
                else:
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
                try:
                    stock_pcs = Product.objects.get(
                        product_id=product_id).stock_pcs
                except:
                    messages.error(request, 'Internal error!')
                else:
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
        # print(form.cleaned_data)
        product_id = form.cleaned_data['product_id']
        customer_id = form.cleaned_data['customer_id']
        qty = form.cleaned_data['qty']

        if request.is_stock_pcs_enough and request.has_passed_vip_check:
            try:
                product = Product.objects.get(product_id=product_id)
                customer = Customer.objects.get_or_create(
                    customer_id=customer_id)[0]
                order_data = {
                    'product_id': product,
                    'qty': qty,
                    'price': product.price * qty,
                    'shop_id': product.shop_id,
                    'customer_id': customer,
                }
                order = Order.objects.create(**order_data)
                # print(order)
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
        order = Order.objects.get(order_id=order_id)
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


def get_top_3_products(request):
    top3 = Order.objects.values('product_id').annotate(
        total=Sum('qty')).order_by('-total')[:3]
    # print(top3)
    data = {}
    for i, product in enumerate(top3, start=1):
        data[i] = product
    # print(data)
    return JsonResponse(data)


def get_shop_statistics(request):
    shops = {}
    for order in Order.objects.all():
        shop_id = str(order.shop_id)
        if shop_id in shops:
            shop = shops[shop_id]
            shop['total_dollars'] += order.price
            shop['total_sold_items'] += order.qty
            shop['order_count'] += 1
        else:
            shops[shop_id] = {
                'total_dollars': order.price,
                'total_sold_items': order.qty,
                'order_count': 1,
            }
    # print(shops)
    return JsonResponse(shops)
