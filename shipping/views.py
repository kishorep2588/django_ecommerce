from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView, DeleteView, CreateView
from django.http import JsonResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


from . forms import PaymentForm
from . models import ShippingInfo, Order, OrderItem, UserPayment
from cart.cart import Cart

from django.contrib.auth.models import User

import datetime
import stripe
from django.conf import settings

import time

# Create your views here.
class ShippingInfoView(ListView):
    model = ShippingInfo
    template_name = 'shipping_info.html'
    context_object_name = 'shipping_info'

class ShippingInfoEditView(UpdateView):
    model = ShippingInfo
    template_name = 'shipping_update.html'
    context_object_name = 'shipping_update'
    fields = '__all__'
    
    def get_success_url(self) -> str:
        return reverse_lazy('shipping_info')
    
def ShippingInfoDelete(request, pk):
    shipping_info = get_object_or_404(ShippingInfo, pk=pk)
    shipping_info.delete()
    return redirect('shipping_info')


class ShippingAddressCreateView(CreateView):
    template_name = 'shipping_create.html'
    model = ShippingInfo
    fields = '__all__'

    success_url = reverse_lazy('shipping_info')

    def form_valid(self, form):
        return super(ShippingAddressCreateView, self).form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('shipping_info')
    

    
def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total = cart.cart_total()

    shipping_address = ShippingInfo.objects.all()

    if request.method == 'POST':
        address_id = request.POST.get('selected_address')
        selected_address = ShippingInfo.objects.get(pk=address_id)
    else:
        selected_address = None
    return render(request, 'checkout.html', {'cart_products':cart_products, 
                                             'quantities':quantities, 
                                             'totals':total,
                                             'shipping_address':shipping_address,
                                             'selected_address':selected_address})

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.cart_total()
        address_id = request.POST.get('selected_address')
        selected_address = ShippingInfo.objects.get(pk=address_id)

        ## Creating Session
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping


        billing_form = PaymentForm()

        return render(request, 'billing_info.html', {'cart_products':cart_products, 
                                             'quantities':quantities, 
                                             'totals':total,
                                             'selected_address':selected_address,
                                             'billing_form':billing_form})
    else:
        messages.success(request, 'Please select an address')
        return redirect('home')
    

def process_order(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    domain_url = 'http://localhost:8000'

    if request.method == 'GET':
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.cart_total()

        my_shipping = request.session.get('my_shipping')
        selected_address = ShippingInfo.objects.get(pk=my_shipping['selected_address'])
        total_quantity = 0

        full_name = selected_address.full_name
        email = selected_address.email

        shipping_address = f'''{selected_address.full_name}
                            {selected_address.address1}
                            {selected_address.address2}
                            {selected_address.city}
                            {selected_address.state}
                            {selected_address.zipcode}
                            {selected_address.country}
                            {selected_address.phone}
                            {selected_address.email}'''
        amount_paid = total
        date_ordered = datetime.datetime.now()
        
        create_order = Order(order_full_name=full_name,
                            order_email=email,
                            order_shipping_address=shipping_address,
                            amount_paid=amount_paid,
                            date_ordered=date_ordered)
        create_order.save()

        ## Getting the Order id
        order_id = create_order.pk

        for product in cart_products:
            product_id = product.id

            if product.is_sale:
                price = product.sale_price
            else:
                price = product.price
            
            for key, value in quantities.items():
                if int(key) == product_id:
                    create_order_item = OrderItem(order_id=order_id,
                                                order=create_order,
                                                product=product,
                                                quantity=value,
                                                price=price)
                    create_order_item.save()
                    total_quantity += 1

        checkout_session = stripe.checkout.Session.create(
			payment_method_types = ['card'],
			line_items = [
				{
					'price_data': {
                        "currency":'USD',
                        "unit_amount":int(total),   ## Stripe expects payment in Cents
                    "product_data":{
                        "name":"Order Checkout",
                        "description":"Checking Out Order through Stripe"
                    },
                    },
					'quantity': total_quantity,
				},
			],
			mode = 'payment',
			customer_creation = 'always',
			success_url = domain_url+'/shipping/payment_success?session_id={CHECKOUT_SESSION_ID}',
			cancel_url = domain_url + '/shipping/payment_cancel',
		)

        for key in list(request.session.keys()):
            if key == 'session_key':
                del request.session[key]
        
        return redirect(checkout_session.url, code=303)

    # if request.POST:
    #     cart = Cart(request)
    #     cart_products = cart.get_prods()
    #     quantities = cart.get_quants()
    #     total = cart.cart_total()
    #     payment_form = PaymentForm(request.POST or None)
    #     my_shipping = request.session.get('my_shipping')
    #     selected_address = ShippingInfo.objects.get(pk=my_shipping['selected_address'])
    #     total_quantity = 0

    #     full_name = selected_address.full_name
    #     email = selected_address.email

    #     shipping_address = f'''{selected_address.full_name}
    #                         {selected_address.address1}
    #                         {selected_address.address2}
    #                         {selected_address.city}
    #                         {selected_address.state}
    #                         {selected_address.zipcode}
    #                         {selected_address.country}
    #                         {selected_address.phone}
    #                         {selected_address.email}'''
    #     amount_paid = total
    #     date_ordered = datetime.datetime.now()
        
    #     create_order = Order(order_full_name=full_name,
    #                         order_email=email,
    #                         order_shipping_address=shipping_address,
    #                         amount_paid=amount_paid,
    #                         date_ordered=date_ordered)
    #     create_order.save()

    #     ## Getting the Order id
    #     order_id = create_order.pk

    #     for product in cart_products:
    #         product_id = product.id

    #         if product.is_sale:
    #             price = product.sale_price
    #         else:
    #             price = product.price
            
    #         for key, value in quantities.items():
    #             if int(key) == product_id:
    #                 create_order_item = OrderItem(order_id=order_id,
    #                                             order=create_order,
    #                                             product=product,
    #                                             quantity=value,
    #                                             price=price)
    #                 create_order_item.save()
    #                 total_quantity += 1

    #     checkout_session = stripe.checkout.Session.create(
	# 		payment_method_types = ['card'],
	# 		line_items = [
	# 			{
	# 				'price_data': {
    #                     "currency":'USD',
    #                     "unit_amount":int(total),   ## Stripe expects payment in Cents
    #                 "product_data":{
    #                     "name":"Order Checkout",
    #                     "description":"Checking Out Order through Stripe"
    #                 },
    #                 },
	# 				'quantity': total_quantity,
	# 			},
	# 		],
	# 		mode = 'payment',
	# 		customer_creation = 'always',
	# 		success_url = domain_url+'/shipping/payment_success?session_id={CHECKOUT_SESSION_ID}',
	# 		cancel_url = domain_url + '/shipping/payment_cancel',
	# 	)

    #     print('checkout_url',checkout_session.url)
        
    #     return redirect(checkout_session.url, code=303)

    else:
        messages.success(request, 'Access Denied')
        return redirect('home')
    
def payment_success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user.id
    if user_id is not None:
        user = User.objects.get(pk=user_id)
        user_payment = UserPayment()
        user_payment.user = user
        user_payment.stripe_checkout_id = checkout_session_id
        user_payment.save()
        return render(request, 'payment_success.html', {'customer': customer})
    else:
        messages.success(request, 'User Not Logged in')
        return redirect('home')


def payment_failure(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	return render(request, 'payment_failure.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        user_payment.payment_bool = True
        user_payment.save()
        print('Session',session)
            
    return HttpResponse(status=200)