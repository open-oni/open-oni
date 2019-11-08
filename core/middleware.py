import os

from django.conf import settings
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers
from django.utils.deprecation import MiddlewareMixin


class DisableClientSideCachingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response


class HttpResponseServiceUnavailable(HttpResponse):
    status_code = 503


class TooBusyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        one, five, fifteen = os.getloadavg()
        if one > settings.TOO_BUSY_LOAD_AVERAGE:
            return HttpResponseServiceUnavailable("""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Server Too Busy</title>
  </head>
  <body>
    <article>
      <h1>Server Too Busy</h1>
      <div>
        <p>Please try your request again shortly.</p>
      </div>
    </article>
  </body>
</html>
""")
        return None
