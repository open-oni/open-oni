from django.conf import settings
from django.utils.http import urlquote

# Enums / constants for telling image_server_for_page which URL prefix to use
RESIZE = 0
TILE = 1

def thumb_image_url(page):
    return resize_url(page, settings.THUMBNAIL_WIDTH)

def medium_image_url(page):
    return resize_url(page, 550)

def resize_url(page, size):
    return  "%s/full/%d,/0/default.jpg" % (image_server_for_page(RESIZE, page), size)

def specific_tile_url(page, w, h, x1, y1, x2, y2):

    w, h, x1, y1, x2, y2 = list(map(int, [w, h, x1, y1, x2, y2]))
    return "%s/%d,%d,%d,%d/%d,%d/0/default.jpg" % (image_server_for_page(TILE, page), x1, y1, x2-x1, y2-y1, w, h)

def image_server_for_page(server_type, page):
    server = ""
    if server_type == RESIZE:
        server = settings.RESIZE_SERVER
    if server_type == TILE:
        server = settings.TILE_SERVER

    return "%s/%s" % (server, urlquote(page.relative_image_path, safe=""))

def iiif_info_for_page(page):
    return "%s" % (image_server_for_page(TILE, page))
