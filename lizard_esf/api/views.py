# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
"""
API views not coupled to models.
"""

from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict

from djangorestframework.response import Response
from djangorestframework import status
from djangorestframework.views import View

from lizard_esf.models import Configuration
from lizard_esf.models import AreaConfiguration
from lizard_esf.models import ValueType
from lizard_esf.models import ConfigurationType
from lizard_esf.models import tree

from lizard_esf.forms import ConfigurationForm
from lizard_esf.forms import NameForm

from lizard_area.models import Area

import json


class TreeView(View):
    """
    Specialized view for reading and updating objects in a treeform.
    """
    def get(self, request):
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        return ['test']


class RootView(View):
    """
    Startpoint.
    """
    def get(self, request):
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        return [{
            'configurations': reverse(
                'lizard_esf_api_configuration_root'),
        }, {
            'configuration types': reverse(
                'lizard_esf_api_configuration_type_root'),
        }, {
            'value types': reverse(
                'lizard_esf_api_value_type_root'),
        }, {
            'tree': reverse(
                'lizard_esf_api_configuration_tree'),
        }]


class ConfigurationListView(View):
    def get(self, request):
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        configs = Configuration.objects.all()
        return [(c.name, c.get_absolute_url) for c in configs]


class ConfigurationCreateView(View):
    """
    Custom view for the creation of configurations.
    """
    form = ConfigurationForm

    def get(self, request):
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        return Response(status.HTTP_200_OK)

    def put(self, request):
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

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
    """
    Configuration details
    """
    def get(self, request, pk):
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        cnf = Configuration.objects.get(pk=pk)
        # Beware, model_to_dict does not include
        # fields that have editable=False
        return model_to_dict(cnf, exclude=['path', 'numchild', 'depth'])

    def delete(self, request, pk):
        """Delete the configuration."""
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        Configuration.objects.get(pk=pk).delete()
        return Response(status.HTTP_200_OK)

class ConfigurationTreeView(View):
    """
    Treeview, basically a dump_bulk() from treebeard
    """
    def get(self, request):
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        area =  request.GET.get('object_id', None)
        area = Area.objects.get(ident=area)
        configs = Configuration.objects.exclude(esf_areaconfiguration_set__area=area)

        print('%i nieuwe configs voor dit gebied'%configs.count())
        for config in configs:
            AreaConfiguration.objects.get_or_create(configuration=config, area=area)


        area_config = AreaConfiguration.objects.filter(area=area).order_by('configuration__name')

        tree_data = tree(area_config)

        return tree_data

    def post(self, request, pk=None):
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        data = json.loads(self.CONTENT.get('data', []))
        if type(data) == dict:
            data = [data]
        for record in data:
            area_config = AreaConfiguration.objects.get(id=int(record['id']))
            del record['id']
            for (key, value) in record.items():
                setattr(area_config, key, value)
            area_config.save()

        return {'success': True}


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
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        return [d.get_dict(url=True)
                for d in self.document.objects.all()]

    def post(self, request):
        """Create a document."""
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        obj = self.document(**self.CONTENT)
        obj.save()
        return Response(status.HTTP_201_CREATED)


class ValueTypeRootView(DocumentRootView):
    """
    View all value types.
    """
    document = ValueType
    form = NameForm


class ConfigurationTypeRootView(DocumentRootView):
    """
    View all configuration types.
    """
    document = ConfigurationType
    form = NameForm


class DocumentView(View):
    """
    Baseview for detail views.

    Subclasses must set form and document attributes.
    """
    def get(self, request, pk):
        """Read a document."""
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        try:
            obj = self.document.objects.get(pk=pk)
        except self.document.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

        if request.GET.get('_format') == 'property':
            fields = request.GET.get('_fields')
            if fields:
                properties = fields.split(',')
            else:
                properties = None
            property_list = obj.get_property_list(properties=properties)
            return {'properties': property_list}

        return obj.get_dict()

    def put(self, request, pk):
        """Update a document."""
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        try:
            obj = self.document.objects.get(pk=pk)
            obj.__dict__.update(self.CONTENT)
            obj.save()
            return Response(status.HTTP_200_OK)
        except self.document.DoesNotExist:
            obj = self.document(pk=pk, **self.CONTENT)
            obj.save()
            return Response(status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """Delete a document."""
        if request.user.is_anonymous():
            return Response(status.HTTP_403_FORBIDDEN)

        self.document.objects.get(pk=pk).delete()
        return Response(status.HTTP_200_OK)


class ValueTypeView(DocumentView):
    """
    Edit value type details.
    """
    document = ValueType
    form = NameForm


class ConfigurationTypeView(DocumentView):
    """
    Edit configuration type details.
    """
    document = ConfigurationType
    form = NameForm
