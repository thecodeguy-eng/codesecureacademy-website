from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def naira(value):
    """Formats a Naira amount consistently: 5000.00 -> '5,000', 4999.50 ->
    '4,999.50'. Used everywhere a price/amount is shown (prefixed with ₦ in
    the template) instead of raw Decimal output, which has no thousands
    separator and always shows two decimal places even on whole amounts."""
    try:
        d = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return value
    if d == d.to_integral_value():
        return "{:,.0f}".format(d)
    return "{:,.2f}".format(d)
