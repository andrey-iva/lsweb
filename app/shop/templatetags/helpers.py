from django import template
from decimal import Decimal
register = template.Library()

# d|get_key:k
@register.filter
def get_key(d, k):
    return str(k) in d

@register.filter
def get_quantity(d, k):
    return d[str(k)]['quantity']

@register.filter
def get_product_total_price_install(d, k):
    return d[str(k)]['total_price_install']

@register.filter
def get_install_price(d, k):
	if str(k) in d:
		return int( float(d[str(k)]['price_install']) ) > 0
	else:
		return False

@register.filter
def add(left, right):
    return str(Decimal(left) + Decimal(right))