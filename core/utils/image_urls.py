from django.conf import settings

def thumb_image_url(page):
    # TODO: FIX THIS!  Use a real URL lib, use IIIF, etc
    return settings.RESIZE_SERVER + "/" + page.relative_image_path + "/%dx%d" % (settings.THUMBNAIL_WIDTH, 0)

def medium_image_url(page):
    # TODO: FIX THIS!  Use a real URL lib, use IIIF, etc
    return settings.RESIZE_SERVER + "/" + page.relative_image_path + "/%dx%d" % (550, 0)
