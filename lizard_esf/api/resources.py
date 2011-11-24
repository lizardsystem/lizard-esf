"""
Model resources for API.
"""
from djangorestframework.resources import ModelResource

from lizard_esf.models import ConfigurationType
from lizard_esf.models import ValueType
from lizard_esf.models import AreaConfiguration

from lizard_esf.forms import NameForm


class ConfigurationTypeResource(ModelResource):
    """
    ConfigurationTypeResource
    """
    form = NameForm
    model = ConfigurationType


class ValueTypeResource(ModelResource):
    """
    ValueTypeResource
    """
    form = NameForm
    model = ValueType


class AreaConfigurationResource(ModelResource):
    """
    AreaConfigurationResource
    """
    model = AreaConfiguration
    fields = ()
