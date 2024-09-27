
from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        ## if the user is new
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, product_quantity):
        product_id = str(product.id)
        product_quantity = int(product_quantity)

        if product_id in self.cart:
            print('Already added to cart')
            pass
        else:
            self.cart[product_id] = product_quantity
        self.session.modified = True

    def update(self, product, quantity):
        product_id = str(product)
        product_quantity = quantity

        existing_cart = self.cart
        existing_cart[product_id] = product_quantity
        self.session.modified = True

        updated_cart = self.cart
        return updated_cart
    
    def delete(self,product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True


    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def cart_total(self):
        quantities = self.cart
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0
        ## {'1':3,'2':5}
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if key == product.id:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
        return total