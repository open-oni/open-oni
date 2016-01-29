from django import template
from openoni.core.utils import image_urls

register = template.Library()

@register.simple_tag
def thumb_image_url(page):
    return image_urls.thumb_image_url(page)

@register.simple_tag
def medium_image_url(page):
    return image_urls.medium_image_url(page)
