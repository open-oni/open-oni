from django.conf import settings

def thumb_image_url(page):
    # TODO: FIX THIS!  Use a real URL lib, use IIIF, etc
    return settings.RESIZE_SERVER + "/" + page.relative_image_path + "/%dx%d" % (settings.THUMBNAIL_WIDTH, 0)

def medium_image_url(page):
    # TODO: FIX THIS!  Use a real URL lib, use IIIF, etc
    return settings.RESIZE_SERVER + "/" + page.relative_image_path + "/%dx%d" % (550, 0)

def specific_tile_url(page, w, h, x1, y1, x2, y2):
    # TODO: FIX THIS!  Use a real URL lib, use IIIF, etc
    return settings.TILE_SERVER + "/" + page.relative_image_path + "/image_%sx%s_from_%s,%s_to_%s,%s.jpg" % (w, h, x1, y1, x2, y2)

def tile_server_for_page(page):
    # TODO: FIX THIS!  Use a real URL lib, use IIIF, etc
    return settings.TILE_SERVER + "/" + page.relative_image_path + "/"
