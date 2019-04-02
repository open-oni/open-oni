# Copy this to urls.py.  Most sites can leave this as-is.  If you have custom
# apps which need routing, modify this file to include those urlconfs.
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
