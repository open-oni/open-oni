import socket
from urllib import urlencode
from urllib2 import urlopen

from django import template
from django.core.cache import cache

register = template.Library()

@register.simple_tag
def get_ext_url(url, timeout=None):
    """
    Used for getting global header and footer
    """
    content = cache.get(url)
    if not content:
        socket_default_timeout = socket.getdefaulttimeout()
        if timeout is not None:
            try:
                socket_timeout = float(timeout)
            except ValueError:
                raise template.TemplateSyntaxError, "timeout argument of geturl tag, if provided, must be convertible to a float"
            try:
                socket.setdefaulttimeout(socket_timeout)
            except ValueError:
                raise template.TemplateSyntaxError, "timeout argument of geturl tag, if provided, cannot be less than zero"
        try:
            try:
                content = urlopen(url).read()
            finally: # reset socket timeout
                if timeout is not None:
                    socket.setdefaulttimeout(socket_default_timeout)
        except:
            content = ''
        # store in cache for 1 day
        cache.set(url, content, 86400)
    return content

@register.simple_tag
def remove_param(aParams, field1, field2=None):
    """
    Given a request.GET or .POST object, shallow clone,
     and remove given fields from the new object
    """
    params = aParams.copy()
    if field1 in params:
        del params[field1]
    if field2 in params:
        del params[field2]
    return urlencode(params)
