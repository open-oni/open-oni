import os

from django.conf import settings
from django.http import HttpResponse


class HttpResponseServiceUnavailable(HttpResponse):
    status_code = 503


class TooBusyMiddleware(object):

    def process_request(self, request):
        one, five, fifteen = os.getloadavg()
        if one > settings.TOO_BUSY_LOAD_AVERAGE:
            return HttpResponseServiceUnavailable("""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Server Too Busy</title> 
  <style></style>
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
