from django.conf import settings
from django.utils.http import urlquote

def thumb_image_url(page):
    return resize_url(page, settings.THUMBNAIL_WIDTH)

def medium_image_url(page):
    return resize_url(page, 550)

def resize_url(page, size):
    return  "%s/full/%d,/0/default.jpg" % (iiif_for_page(page), size)

def specific_tile_url(page, w, h, x1, y1, x2, y2):
    w, h, x1, y1, x2, y2 = list(map(int, [w, h, x1, y1, x2, y2]))
    return "%s/%d,%d,%d,%d/%d,%d/0/default.jpg" % (iiif_for_page(page),
        x1, y1, x2-x1, y2-y1, w, h)

def iiif_for_page(page):
    return "%s/%s" % (settings.IIIF_URL, urlquote(page.relative_image_path,
        safe=""))
