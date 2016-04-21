from django.conf import settings

from django.utils.http import urlquote

def thumb_image_url(page):
    return tile_server_for_page(page) + "/full/%d,/0/default.jpg" % settings.THUMBNAIL_WIDTH

def medium_image_url(page):
    return tile_server_for_page(page) + "/full/550,/0/default.jpg"

def specific_tile_url(page, w, h, x1, y1, x2, y2):
    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
    return tile_server_for_page(page) + "/%d,%d,%d,%d/%d,%d/0/default.jpg" % (x1, y1, x2-x1, y2-y1, w, h)
    
def tile_server_for_page(page):
    return settings.IIIF_SERVER + "/" + urlquote(page.relative_image_path, safe="")
