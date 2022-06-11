from decimal import Decimal
from . import CART_SESSION_ID
from .models import Product

import logging

class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            
            item['price_install'] = Decimal(item['price_install'])
            item['total_price_install'] = Decimal(item['price_install']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False, install=0, loop=None):
        
        logging.debug("Cart add product: %s, quantity: %s, override_quantity: %s, install: %s, loop: %s", 
            product, 
            quantity, 
            override_quantity, 
            install, 
            loop)

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        if install:
            self.cart[product_id]['price_install'] = str(Decimal(product.price_install))
        else:
            self.cart[product_id]['price_install'] = '0'
        
        if loop == 'on':
            self.cart[product_id]['loop'] = loop
        
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        products_price = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        install_price = sum(Decimal(item['price_install']) * item['quantity'] for item in self.cart.values())
        return products_price + install_price

    def get_products_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_products_install_total_price(self):
        return sum(Decimal(item['price_install']) * item['quantity'] for item in self.cart.values())