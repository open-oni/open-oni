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
