from atexit import register
from django import template

register = template.Library()

@register.filter
def replaceSeparator(string):
    return string.replace('|', ' | ')

