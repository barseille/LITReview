# blog/templatetags.py

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def classname(obj):
    return obj.__class__.__name__