from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def remove_param(context, *args):
    """Remove keys from the GET object and return a new URL"""
    request = context["request"]
    params = request.GET.copy()
    for arg in args:
        if arg in params:
            del params[arg]
    return params.urlencode()

@register.simple_tag(takes_context=True)
def remove_param_value(context, key, value):
    """Remove a key/value pair from the GET request and return a new URL"""
    request = context["request"]
    params = request.GET.copy()
    if key in params:
        args = params.getlist(key)
        if value in args:
            args.remove(value)
            params.setlist(key, args)

    return params.urlencode()
