"""
API views not coupled to models.
"""
from django.core.urlresolvers import reverse

from djangorestframework.views import View

from lizard_esf.models import ConfigurationType
from lizard_esf.models import ValueType
from lizard_esf.models import Configuration
from lizard_esf.models import AreaConfiguration


class RootView(View):
    """
    Startpoint.
    """
    def get(self, request):
         return {
            "configuration types": reverse(
                'lizard_esf_api_configuration_type_root'),
            "value types": reverse(
                'lizard_esf_api_value_type_root'),
            "configurations": reverse(
                'lizard_esf_api_configuration_root'),
            "area configurations": reverse(
                'lizard_esf_api_area_configuration_root'),
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


class ConfigurationTypeRootView(DocumentRootView):
    """
    View all configuration types.
    """
    document = ConfigurationType


class ValueTypeRootView(DocumentRootView):
    """
    View all value types.
    """
    document = ValueType


class ConfigurationRootView(DocumentRootView):
    """
    View all configurations.
    """
    document = Configuration


class AreaConfigurationRootView(DocumentRootView):
    """
    View all area configurations.
    """
    document = AreaConfiguration
