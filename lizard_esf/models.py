# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import re

from django.core.urlresolvers import reverse
from django.db import models

from lizard_area.models import Area
from treebeard.mp_tree import MP_Node

# from django.core.urlresolvers import reverse
# from lizard_fewsnorm.models import TimeseriesKeys


def uncamel(model_name):
    """
    Convert some model name into an underscore-style name.
    """
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', model_name).lower()


class NameAbstract(models.Model):
    """
    Abstract model with only a name as property.
    """
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        abstract = True
        ordering = ['id']

    def __unicode__(self):
        return self.name

#   def get_absolute_url(self):
#   """
#   Return absolute url for use in api.

#   Convenient when creating manual listviews; djangorestframework does
#   so automatically.
#   """
#       return reverse('lizard_esf_api_' +
#                      uncamel(self.__class__.__name__),
#                      kwargs={'pk': self.pk})


class ConfigurationType(NameAbstract):
    """
    Type of waterbalanceconfiguration
    """
    pass


class ValueType(NameAbstract):
    """
    Type of value
    """
    pass


class Configuration(MP_Node):
    """
    Waterbalanceconfiguration.
    """
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128)
    short_name = models.CharField(max_length=128)
    source_name = models.CharField(max_length=128)
    configuration_type = models.ForeignKey(ConfigurationType)

    default_parameter_code_manual_fews = models.CharField(max_length=128)
    default_parameter_code_automatic_fews = models.CharField(max_length=128)
    default_parameter_code_final_fews = models.CharField(max_length=128)
    value_type = models.ForeignKey(ValueType)

    expanded = models.BooleanField(default=False)

    node_order_by = ['name']

    def get_absolute_url(self):
        return reverse(
            'lizard_esf_api_configuration_detail',
            kwargs={'pk': self.pk},
        )

    def __unicode__(self):
        return self.name


class AreaConfiguration(models.Model):
    """
    Areaconfiguration.
    """
    area = models.ForeignKey(Area, related_name='esf_areaconfiguration_set')
    configuration = models.ForeignKey(
        Configuration,
        related_name='esf_areaconfiguration_set',
    )
    manual = models.IntegerField(default=1)
    manual_value = models.FloatField(
        blank=True, null=True,
    )
    last_edit_by = models.CharField(max_length=256, blank=True, default='-')
    last_edit_date = models.DateTimeField(auto_now=True)
    last_comment = models.CharField(max_length=256, blank=True, default='-')

#    timeseries_manual = models.ForeignKey(
#        TimeseriesKeys,
#        related_name='esf_areaconfiguration_set1',
#    )
#    timeseries_automatic = models.ForeignKey(
#        TimeseriesKeys,
#        related_name='esf_areaconfiguration_set2',
#    )
#    timeseries_final_value = models.ForeignKey(
#        TimeseriesKeys,
#        related_name='esf_areaconfiguration_set3',
#    )

    def get_mydump(self):
        return {
            'id': self.id,
            'config_id': self.configuration.id,
            'name': self.configuration.name,
            'source_name': self.configuration.source_name,
            'manual': self.manual,
            'manual_value': self.manual_value,
            'auto_value': 2,
            'type': self.configuration.value_type.name,
            'last_comment': 'ja ja ja',
        }


def tree(config):
    a = {}
    for b in config:
        if b.configuration.get_parent():
            parent_id = b.configuration.get_parent().id
        else:
            parent_id = None
            pass
        config_id = b.configuration.id

        if not parent_id in a:
            a[parent_id] = []
        if not config_id in a:
            a[config_id] = []
        a[parent_id].append(b.get_mydump())

    tree = {'id': -1, 'name': 'root'}

    tree['children'] = a[None]

    for child in tree['children']:

        child['children'] = a[child['config_id']]

        for child_1 in child['children']:
            child_1['children'] = a[child_1['config_id']]

            for child_2 in child_1['children']:
                child_2['children'] = a[child_2['config_id']]

                for child_3 in child_2['children']:
                    child_3['children'] = a[child_3['config_id']]

    return tree
