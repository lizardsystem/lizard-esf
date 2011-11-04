from django.contrib.gis import admin

from lizard_esf.models import Configuration


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'value_type')


admin.site.register(Configuration, ConfigurationAdmin)


