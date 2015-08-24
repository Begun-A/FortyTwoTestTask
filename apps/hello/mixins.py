from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect


class JsonResponse(HttpResponse):
    """
        JSON response
    """
    def __init__(
        self, content, mimetype='application/json',
        status=None, content_type=None
    ):
        super(JsonResponse, self).__init__(
            content=simplejson.dumps(content),
            mimetype=mimetype,
            status=status,
            content_type=content_type,
        )


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
            return HttpResponseRedirect(self.get_success_url())
        else:
            return response
