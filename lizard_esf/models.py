# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.db import models

from lizard_area.models import Area
from lizard_fewsnorm import TimeSeriesKeys


class NameAbstract(models.Model):
    """
    Abstract model with only a name as property.
    """
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

class ConfigurationType(NameAbstract)
    """
    Type of waterbalanceconfiguration
    """
    pass


class ValueType(NameAbstract)
    """
    Type of value
    """
    pass


class Configuration(models.Model)
    """
    Waterbalanceconfiguration.
    """
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128)
    parent = models.ForeignKey('Category', blank=True, null=True)
    short_name = models.CharField(max_length=128)
    source_name = models.CharField(max_length=128)
    configuration_type = models.ForeignKey(ConfigurationType)

    default_parameter_code_manual_fews =  models.CharField(max_length=128)
    default_parameter_code_automatic_fews = models.CharField(max_length=128)
    default_parameter_code_final_fews = models.CharField(max_length=128)
    value_type = models.ForeignKey(valueType)


class AreaConfiguration(models.Model)
    """
    Areaconfiguration.
    """
    area = models.ForeignKey(Area)
    configuration = models.ForeignKey(Configuration)
    manual = models.BooleanField()
    manual_value = models.DecimalField()
    timeseries_manual = models.ForeignKey(TimeSeriesKeys)
    timeseries_automatic = models.ForeignKey(TimeSeriesKeys)
    timeseries_final_value = models.ForeignKey(TimeSeriesKeys)
