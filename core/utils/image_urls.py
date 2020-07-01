from django.conf import settings
from django.utils.http import urlquote

def thumb_image_url(page):
    return resize_url(page, settings.THUMBNAIL_WIDTH)

def resize_url(page, size):
    return  "%s/full/%d,/0/default.jpg" % (page_iiif_info_url(page), size)

def specific_tile_url(page, w, h, x1, y1, x2, y2):
    w, h, x1, y1, x2, y2 = list(map(int, [w, h, x1, y1, x2, y2]))
    return "%s/%d,%d,%d,%d/%d,%d/0/default.jpg" % (page_iiif_info_url(page),
        x1, y1, x2-x1, y2-y1, w, h)

def page_iiif_info_url(page):
    # This is a hack to avoid crashing when there's no image.  It's an invalid
    # value, but it doesn't crash, so it's better than nothing.
    if page.relative_image_path is None:
        return "%s/None" % settings.IIIF_URL
    else:
        return "%s/%s" % (settings.IIIF_URL, urlquote(page.relative_image_path, safe=""))
