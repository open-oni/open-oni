# Copy this to urls.py.  Most sites can leave this as-is.  If you have custom
# apps which need routing, modify this file to include those urlconfs.
from django.conf.urls import url, include

urlpatterns = [
  url('', include("core.urls")),
  # url('map/', include("statemap.urls"))
]
