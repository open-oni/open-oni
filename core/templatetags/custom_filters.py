from django import template
from django.template.defaultfilters import stringfilter

from rfc3339 import rfc3339

from core.utils import url
from core.utils.utils import label


register = template.Library()


@register.filter(name='label')
def _label(value):
    return label(value)


@register.filter(name='pack_url')
def pack_url(value, default='-'):
    return url.pack_url_path(value, default)


@register.filter(name='rfc3339')
def rfc3339_filter(d):
    return rfc3339(d)


@register.filter
@stringfilter
# from https://stackoverflow.com/a/18951166/4154134
def template_exists(value):
    try:
        template.loader.get_template(value)
        return True
    except template.TemplateDoesNotExist:
        return False
