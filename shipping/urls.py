from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShippingInfoView.as_view(), name='shipping_info'),
    path('update/<int:pk>/', views.ShippingInfoEditView.as_view(), name='shipping_update'),
    path('delete/<int:pk>/', views.ShippingInfoDelete, name='shipping_delete'),
    path('create/', views.ShippingAddressCreateView.as_view(), name='shipping_create'),
    path('checkout/', views.checkout, name='checkout'),
    path('billing_info/', views.billing_info, name='billing_info'),
    path('process_order/', views.process_order, name='process_order'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failure/', views.payment_failure, name='payment_failure'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook')
]
