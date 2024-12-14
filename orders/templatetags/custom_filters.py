# orders/templatetags/custom_filters.py

from django import template

# Registering the filter so it can be used in templates
register = template.Library()

# Define the multiply filter
@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return value * arg
    except TypeError:
        return 0  # If the values can't be multiplied, return 0


@register.filter(name='currency')
def currency(value):
    try:
        return f"Rp {value:,.0f}"  # Formats the value in Indonesian Rupiah
    except (TypeError, ValueError):
        return value

@register.filter(name='rupiah')
def rupiah(value):
    return f"Rp {value:,.0f}".replace(',', '.')