from django import template
from core.utils import image_urls

register = template.Library()

@register.simple_tag
def custom_size_image_url(page, size):
  return image_urls.resize_url(page, size)

@register.simple_tag
def tiny_image_url(page):
    return image_urls.resize_url(page, 120)

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
def iiif_info(page):
    return image_urls.page_iiif_info_url(page)
