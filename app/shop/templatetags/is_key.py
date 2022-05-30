from django import template

register = template.Library()

# d|get_key:k
@register.filter
def get_key(d, k):
    return str(k) in d

@register.filter
def get_install_price(d, k):
	if str(k) in d:
		return int( float(d[str(k)]['price_install']) ) > 0
	else:
		return False