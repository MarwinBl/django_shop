from django import template

register = template.Library()

PAGINATOR_PREFIX = '?page='


@register.filter(name='paginator')
def paginator(string):
    string = str(string)
    if string.startswith(PAGINATOR_PREFIX):
        return string
    else:
        return f'{PAGINATOR_PREFIX}{string}'
