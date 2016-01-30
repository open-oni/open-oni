from django import template
from openoni.core.utils import image_urls

register = template.Library()

@register.simple_tag
def thumb_image_url(page):
    return image_urls.thumb_image_url(page)

@register.simple_tag
def medium_image_url(page):
    return image_urls.medium_image_url(page)

@register.simple_tag
def specific_tile_url(page, w, h, x1, y1, x2, y2):
    return image_urls.specific_tile_url(page, w, h, x1, y1, x2, y2)

@register.simple_tag
def tile_server_for_page(page):
    return image_urls.tile_server_for_page(page)
