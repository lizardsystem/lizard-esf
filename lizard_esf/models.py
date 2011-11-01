# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.db import models

from lizard_area.models import Area
from lizard_fewsnorm.models import TimeseriesKeys


class NameAbstract(models.Model):
    """
    Abstract model with only a name as property.
    """
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

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


class Configuration(models.Model):
    """
    Waterbalanceconfiguration.
    """
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128)
    parent = models.ForeignKey('self', blank=True, null=True)
    short_name = models.CharField(max_length=128)
    source_name = models.CharField(max_length=128)
    configuration_type = models.ForeignKey(ConfigurationType)

    default_parameter_code_manual_fews = models.CharField(max_length=128)
    default_parameter_code_automatic_fews = models.CharField(max_length=128)
    default_parameter_code_final_fews = models.CharField(max_length=128)
    value_type = models.ForeignKey(ValueType)


class AreaConfiguration(models.Model):
    """
    Areaconfiguration.
    """
    area = models.ForeignKey(Area, related_name='esf_areaconfiguration_set')
    configuration = models.ForeignKey(Configuration, related_name='esf_areaconfiguration_set')
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
