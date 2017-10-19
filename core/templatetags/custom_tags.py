from django import template
from urllib import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def remove_param(context, *args):
    """
    Given a request.GET or .POST object, shallow clone,
     and remove list of fields from the new object
    """
    request = context["request"]
    params = request.GET.copy()
    for arg in args:
        if arg in params:
            del params[arg]
    return urlencode(params)

@register.simple_tag(takes_context=True)
def remove_param_value(context, key, value):
    """Given a request.GET or .POST object, shallow clone,
    and remove a single key/value pair"""
    request = context["request"]
    params = request.GET.copy()
    if key in params:
        args = params.getlist(key)
        if value in args:
            args.remove(value)
            params.setlist(key, args)

    return params.urlencode()
