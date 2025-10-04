from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
import stripe
import json

from .models import Product, Order, OrderItem


if settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def index(request):
   
    products = Product.objects.filter(is_active=True)[:3]  
    

    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, status='paid')
    else:

        orders = Order.objects.filter(status='paid')
    
    context = {
        'products': products,
        'orders': orders,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'stripe_configured': bool(settings.STRIPE_PUBLIC_KEY and settings.STRIPE_SECRET_KEY),
    }
    return render(request, 'payments/index.html', context)


@require_POST
def create_checkout_session(request):
    try:
      
        quantities = {}
        total_amount = Decimal('0.00')
        line_items = []
        order_items = []
        
        products = Product.objects.filter(is_active=True)[:3]
        
        for product in products:
            qty_key = f'quantity_{product.id}'
            quantity = int(request.POST.get(qty_key, 0))
            
            if quantity > 0:
                quantities[product.id] = quantity
                item_total = product.price * quantity
                total_amount += item_total

                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(product.price * 100),  # Convert to cents
                        'product_data': {
                            'name': product.name,
                            'description': product.description,
                        },
                    },
                    'quantity': quantity,
                })

                order_items.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_price': float(product.price),
                    'quantity': quantity,
                    'subtotal': float(item_total),
                })
        
        if not line_items:
            messages.error(request, 'Please select at least one product with quantity > 0')
            return redirect('index')

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            status='pending',
            total_amount=total_amount,
            items_json=json.dumps(order_items)
        )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=settings.SITE_URL + '/success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.SITE_URL + '/cancel/',
            metadata={
                'order_id': order.id,
            },
        )

        order.session_id = checkout_session.id
        order.save()

        return redirect(checkout_session.url)
        
    except Exception as e:
        messages.error(request, f'Error creating checkout session: {str(e)}')
        return redirect('index')


def success(request):
    """Handle successful payment"""
    session_id = request.GET.get('session_id')
    
    if not session_id:
        messages.error(request, 'Invalid session')
        return redirect('index')
    
    try:

        checkout_session = stripe.checkout.Session.retrieve(session_id)
        
        order = Order.objects.get(session_id=session_id)
        
        if order.status == 'paid':
            messages.info(request, 'Order already processed!')
            return render(request, 'payments/success.html', {'order': order})
        
        with transaction.atomic():
            order.status = 'paid'
            order.stripe_payment_intent = checkout_session.payment_intent
            order.save()
            
            items_data = order.get_items()
            for item_data in items_data:
                OrderItem.objects.create(
                    order=order,
                    product_id=item_data.get('product_id'),
                    product_name=item_data['product_name'],
                    product_price=Decimal(str(item_data['product_price'])),
                    quantity=item_data['quantity'],
                    subtotal=Decimal(str(item_data['subtotal'])),
                )
        
        messages.success(request, 'Payment successful! Your order has been placed.')
        return render(request, 'payments/success.html', {'order': order})
        
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('index')
    except Exception as e:
        messages.error(request, f'Error processing payment: {str(e)}')
        return redirect('index')


def cancel(request):
    messages.warning(request, 'Payment was cancelled.')
    return render(request, 'payments/cancel.html')


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        order_id = session.get('metadata', {}).get('order_id')
        
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                
                if order.status == 'pending':
                    with transaction.atomic():
                        order.status = 'paid'
                        order.stripe_payment_intent = session.get('payment_intent', '')
                        order.save()
                        
                        if not order.items.exists():
                            items_data = order.get_items()
                            for item_data in items_data:
                                OrderItem.objects.create(
                                    order=order,
                                    product_id=item_data.get('product_id'),
                                    product_name=item_data['product_name'],
                                    product_price=Decimal(str(item_data['product_price'])),
                                    quantity=item_data['quantity'],
                                    subtotal=Decimal(str(item_data['subtotal'])),
                                )
            except Order.DoesNotExist:
                pass
    
    return HttpResponse(status=200)


def my_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, status='paid')
    else:
        orders = Order.objects.filter(status='paid')
    
    return render(request, 'payments/my_orders.html', {'orders': orders})


def status_check(request):
    products = Product.objects.filter(is_active=True)[:3]
    orders = Order.objects.filter(status='paid')
    
    context = {
        'products': products,
        'orders': orders,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'stripe_configured': bool(settings.STRIPE_PUBLIC_KEY and settings.STRIPE_SECRET_KEY),
    }
    return render(request, 'payments/status.html', context)
