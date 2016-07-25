# Copy this to urls.py.  Most sites can leave this as-is.  If you have custom
# apps which need routing, modify this file to include those urlconfs.
from django.conf.urls import url, include

urlpatterns = [

  url('', include("core.urls")),
  # If you were to add a plugin app that handles its own URLs, you might do
  # something like this:
  #
  # url(r'^map/', include("onisite.plugins.map.urls")),
]
