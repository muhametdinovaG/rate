from django.views.generic.base import TemplateView
from .models import Rates


class TemplateViewMixin(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(TemplateViewMixin, self).get_context_data(**kwargs)
        context.update({
            'rate': Rates.objects.first(),
        })
        return context
