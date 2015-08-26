from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import LogWebRequest


class LogRequestView(ListView):

    template_name = 't3_requests/requests.html'
    queryset = LogWebRequest.objects.order_by('-id')[:10]
    context_object_name = 'log_requests'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(LogRequestView, self).dispatch(*args, **kwargs)
