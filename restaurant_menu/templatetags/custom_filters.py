# templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='to_list')
def to_list(start, end):
    return list(range(start, end + 1))
