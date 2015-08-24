from django.core.urlresolvers import reverse
from .models import LogWebRequest


# for selenium purposes:
IGNORE_URL = ('/favicon.ico',)


class LogWebReqMiddleware(object):

    def process_response(self, request, response):

        if (
            request.path != reverse('requests') and
            request.is_ajax() is False and
            request.path not in IGNORE_URL
        ):
            LogWebRequest(
                method=request.method,
                path=request.path,
                status_code=response.status_code,
                remote_addr=request.META['REMOTE_ADDR']
            ).save()
        return response
