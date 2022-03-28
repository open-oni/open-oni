"""openoni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Copy this to urls.py.  Most sites can leave this as-is.  If you have custom
# apps which need routing, modify this file to include those urlconfs.
#
# NOTE: DO NOT try to change the URLs which resolve to pages and titles.
# These are currently set up in ONI in a way that, if changed, can cause the
# application to be unable to find any of your OCR data!  (For details, see
# https://github.com/open-oni/open-oni/issues/556)
from django.urls import include, path, re_path

urlpatterns = [
  # Plugin URLs
  #re_path(r'^map/', include("onisite.plugins.map.urls")),

  # Theme URLs
  #path('', include("themes.(theme_name).urls")),

  # Open ONI URLs
  path('', include("core.urls")),
]
