from django.contrib.gis import admin

from lizard_esf.models import Configuration
from lizard_esf.models import AreaConfiguration
from lizard_esf.models import ValueType
from lizard_esf.models import ConfigurationType
from lizard_esf.models import DbfFile
from lizard_esf.models import DBFConfiguration


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'code',
        #'path',
        #'depth',
        'manual',
        'is_main_esf',
        'configuration_type',
        #'value_type',
        'source_name',
        'base_config',
        'default_parameter_code_manual_fews',
        #'timeserie_ref_status',
        'dbf_file',
        #'dbf_index',
        'dbf_valuefield_name',
        #'dbf_valuefield_type',
        #'dbf_valuefield_length',
        #'dbf_valuefield_decimals',
        'dbf_manualfield_name'
    )

    list_editable = (
        'name',
        'code',
        #'path',
        #'depth',
        'manual',
        'is_main_esf',
        'configuration_type',
        #'value_type',
        'source_name',
        'base_config',
        'default_parameter_code_manual_fews',
        #'timeserie_ref_status',
        'dbf_file',
        #'dbf_index',
        'dbf_valuefield_name',
        #'dbf_valuefield_type',
        #'dbf_valuefield_length',
        #'dbf_valuefield_decimals',
        'dbf_manualfield_name'
    )

    list_filter = ('dbf_file',)
    ordering = ('path',)


admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(AreaConfiguration)
admin.site.register(ValueType)
admin.site.register(ConfigurationType)
admin.site.register(DbfFile)
admin.site.register(DBFConfiguration)
