from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply value by arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return None


@register.filter(name='currency')
def currency(value):
    try:
        return f"Rp {value:,.0f}"  # Formats the value in Indonesian Rupiah
    except (TypeError, ValueError):
        return value

@register.filter(name='rupiah')
def rupiah(value):
    return f"Rp {value:,.0f}".replace(',', '.')