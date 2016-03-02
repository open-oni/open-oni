from django.conf import settings

from django.utils.http import urlquote

def thumb_image_url(page):
    return settings.IIIF_SERVER + "/" + urlquote(page.relative_image_path, safe="") + "/0,0,%s,%s/%s,/0/default.jpg" % (page.jp2_width, page.jp2_length, settings.THUMBNAIL_WIDTH)

def medium_image_url(page):
    return settings.IIIF_SERVER + "/" + urlquote(page.relative_image_path, safe="") + "/0,0,%s,%s/%s,/0/default.jpg" % (page.jp2_width, page.jp2_length, 550)


def specific_tile_url(page, w, h, x1, y1, x2, y2):
    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
    return settings.IIIF_SERVER + "/" + urlquote(page.relative_image_path, safe="") + "/%s,%s,%s,%s/%s,%s/0/default.jpg" % (x1, y1, x2-x1, y2-y1, w, h)
    

def tile_server_for_page(page):
    return settings.IIIF_SERVER + "/" + urlquote(page.relative_image_path, safe="")
