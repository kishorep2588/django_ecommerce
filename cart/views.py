from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product

from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    products = cart.get_prods()
    quantities = cart.get_quants()
    total = cart.cart_total()
    return render(request, 'cart_summary.html', {'cart_products':products, 'quantities':quantities, 'total':total})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        print(product_id)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, product_quantity)
        qty = cart.__len__()
        response = JsonResponse({'qty':qty})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        cart.update(product_id, product_quantity)

        response = JsonResponse({'qty': product_quantity})
        return response


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        cart.delete(product_id)

        return redirect('cart_summary')

