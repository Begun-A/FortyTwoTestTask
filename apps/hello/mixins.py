from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.core.serializers.json import json, DjangoJSONEncoder


class JsonResponse(HttpResponse):
    """
        JSON response
    """
    def __init__(
        self, content,
        status=None, content_type='application/json'
    ):
        super(JsonResponse, self).__init__(
            content=json.dumps(content, cls=DjangoJSONEncoder),
            status=status,
            content_type=content_type,
        )


class LoginRequiredMixin(object):
    """Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            return JsonResponse(
                content=self.data,
                status=200
            )
        else:
            return response
