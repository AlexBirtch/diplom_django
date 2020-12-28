from django import template

register = template.Library()


@register.filter
def get_stars(count):
    i = int(count)
    star = '★'
    return star * i
