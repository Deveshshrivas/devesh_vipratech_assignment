from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('status/', views.status_check, name='status_check'),
]
