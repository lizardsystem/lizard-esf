"""
API views not coupled to models.
"""
from django.core.urlresolvers import reverse

from djangorestframework.views import View

from lizard_esf.models import Configuration


class RootView(View):
    """
    Startpoint.
    """
    def get(self, request):
         return {
            "configurations": reverse(
                'lizard_esf_api_configuration_root'),
            }


class DocumentRootView(View):
    """
    Baseview for root views.

    Subclasses must set the document attribute.
    """
    def get(self, request):
        """
        Read a document list. Assumes documents have a get_absolute_url()
        method implemented.
        """
        return [[d, d.get_absolute_url()]
for d in self.document.objects.all()]


class ConfigurationRootView(DocumentRootView):
    """
    View all annotations.
    """
    document = Configuration
