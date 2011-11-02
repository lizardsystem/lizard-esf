# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django import forms
from django.utils.translation import ugettext

from lizard_esf.models import Configuration
from lizard_esf.models import ConfigurationType
from lizard_esf.models import ValueType


class ConfigurationForm(forms.Form):
    """Form for editing of annotations."""
    name = forms.CharField(
        label=ugettext(u'Name'),
    )
    # References
    configuration_type = forms.ModelChoiceField(
        label=ugettext(u'Configuration type'),
        queryset=ConfigurationType.objects.all(),
        empty_label=None,
    )
    value_type = forms.ModelChoiceField(
        label=ugettext(u'Value type'),
        queryset=ValueType.objects.all(),
        empty_label=None,
    )
    parent = forms.ModelChoiceField(
        label=ugettext(u'Parent configuration'),
        queryset=Configuration.objects.all(),
        required=False,
    )
