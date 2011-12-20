from django.contrib.gis import admin

from lizard_esf.models import Configuration
from lizard_esf.models import AreaConfiguration
from lizard_esf.models import ValueType
from lizard_esf.models import ConfigurationType


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'depth', 'manual', 'value_type')


admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(AreaConfiguration)
admin.site.register(ValueType)
admin.site.register(ConfigurationType)
