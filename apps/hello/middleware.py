from .models import LogWebRequest


class LogWebReqMiddleware(object):

    def process_response(self, request, response):

        LogWebRequest(
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            remote_addr=request.META['REMOTE_ADDR']
        ).save()
        return response
