# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import re

from django.db import models

# from django.core.urlresolvers import reverse

from lizard_area.models import Area
from lizard_fewsnorm.models import TimeseriesKeys

from treebeard.mp_tree import MP_Node


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
    manual = models.BooleanField()
    manual_value = models.DecimalField(max_digits=15, decimal_places=6)
    timeseries_manual = models.ForeignKey(
        TimeseriesKeys,
        related_name='esf_areaconfiguration_set1',
    )
    timeseries_automatic = models.ForeignKey(
        TimeseriesKeys,
        related_name='esf_areaconfiguration_set2',
    )
    timeseries_final_value = models.ForeignKey(
        TimeseriesKeys,
        related_name='esf_areaconfiguration_set3',
    )
