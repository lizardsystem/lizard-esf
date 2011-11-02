"""
Model resources for API.
"""
from djangorestframework.resources import ModelResource

from lizard_esf.models import ConfigurationType
from lizard_esf.models import ValueType
from lizard_esf.models import AreaConfiguration


class ConfigurationTypeResource(ModelResource):
    """
    ConfigurationTypeResource
    """
    model = ConfigurationType
    fields = ()


class ValueTypeResource(ModelResource):
    """
    ValueTypeResource
    """
    model = ValueType
    fields = ()


class AreaConfigurationResource(ModelResource):
    """
    AreaConfigurationResource
    """
    model = AreaConfiguration
    fields = ()
