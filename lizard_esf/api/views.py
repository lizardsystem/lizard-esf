# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
"""
API views not coupled to models.
"""

from django.core.urlresolvers import reverse

from djangorestframework.response import Response
from djangorestframework import status
from djangorestframework.views import View

from lizard_esf.models import Configuration

from lizard_esf.forms import ConfigurationForm

import logging
logger = logging.getLogger(__name__)


class TreeView(View):
    """
    Specialized view for reading and updating objects in a treeform.
    """
    def get(self, request):
        return ['test']


class RootView(View):
    """
    Startpoint.
    """
    def get(self, request):
        return [{
            'configurations': reverse(
                'lizard_esf_api_configuration_root'),
        }, {
            'area configurations': reverse(
                'lizard_esf_api_area_configuration_root'),
        }, {
            'configuration types': reverse(
                'lizard_esf_api_configuration_type_root'),
        }, {
            'value types': reverse(
                'lizard_esf_api_value_type_root'),
        }, {
            'tree': reverse(
                'lizard_esf_api_tree'),
        }]


class ConfigurationListView(View):
    pass


class ConfigurationCreateView(View):
    """
    Custom view for the creation of configurations.
    """
    form = ConfigurationForm

    def get(self, request):
        return Configuration.dump_bulk()
        pass

    def put(self, request):
        parent = self.CONTENT['parent']
        del self.CONTENT['parent']

        if parent:
            # Create a new child under the parent node
            parent.add_child(**self.CONTENT)
            return Response(status.HTTP_200_OK)

        # Add it as a root node
        Configuration.add_root(**self.CONTENT)
        return Response(status.HTTP_200_OK)


class ConfigurationDetailView(View):
    pass


class ConfigurationTreeView(View):
    """
    Treeview, basically a dump_bulk() from treebeard
    """
    def get(self, request):
        return Configuration.dump_bulk()
