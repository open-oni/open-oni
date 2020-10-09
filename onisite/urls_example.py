# Copy this to urls.py.  Most sites can leave this as-is.  If you have custom
# apps which need routing, modify this file to include those urlconfs.
#
# NOTE: DO NOT try to change the URLs which resolve to pages and titles.
# These are currently set up in ONI in a way that, if changed, can cause the
# application to be unable to find any of your OCR data!  (For details, see
# https://github.com/open-oni/open-oni/issues/556)
from django.conf.urls import url, include

# Django documentation recommends always using raw string syntax: r''
urlpatterns = [
  # Plugin URLs
  #url(r'^map/', include("onisite.plugins.map.urls")),

  # Theme URLs
  #url(r'', include("themes.(theme_name).urls")),

  # Open ONI URLs
  url(r'', include("core.urls")),
]
