import json
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from hello.models import LogWebRequest
from hello.mixins import JsonResponse


class LogRequestView(ListView):

    template_name = 'requests.html'
    queryset = LogWebRequest.objects.order_by('-id')[:10]
    context_object_name = 'log_requests'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(LogRequestView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return super(LogRequestView, self).get(request, *args, **kwargs)

        if 'priority' in request.GET:
            update_q = LogWebRequest.objects.filter(
                priority=request.GET['priority']
            ).order_by('-id')[:10]
        else:
            update_q = LogWebRequest.objects.order_by('-id')[:10]
        data = json.loads(serializers.serialize('json', update_q))
        return JsonResponse(content=data, status=200)
