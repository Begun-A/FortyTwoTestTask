from django.core.urlresolvers import reverse
from hello.models import LogWebRequest


# for selenium purposes:
IGNORE_LIST = (
    '/favicon.ico',
    '/static'
)


def in_ignore_list(path, ignore_list=IGNORE_LIST):
    for ignore_url in ignore_list:
        if ignore_url in path:
            return True
    return False


class LogWebReqMiddleware(object):

    def process_response(self, request, response):

        if (
            not in_ignore_list(request.path)
            and not request.is_ajax()
            and request.path is not reverse('requests')
        ):
            LogWebRequest(
                method=request.method,
                path=request.path,
                status_code=response.status_code,
                remote_addr=request.META['REMOTE_ADDR']
            ).save()
        return response
