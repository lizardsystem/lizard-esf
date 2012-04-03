# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import logging
import re

from django.core.urlresolvers import reverse
from django.db import models

from lizard_area.models import Area
from treebeard.mp_tree import MP_Node
from lizard_fewsnorm.models import TimeSeriesCache

from lizard_security.models import DataSet

logger = logging.getLogger(__name__)


def uncamel(model_name):
    """
    Convert some model name into an underscore-style name.
    """
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', model_name).lower()


class GettersMixin(object):
    """
    Provides a get_dict() method and a get_absolute_url() method.
    """
    def get_dict(self, url=False, ref_urls=False, ref_objects=False):
        """
        Return the fields and their contents as a dict.

        If url=True, add own absolute url, if ref_urls=True, add urls for any
        referencefields present, if ref_objects, add objects instead of id's
        for ForeignKeys.
        """
        field_names = [field.name for field in self._meta.fields]

        result = dict([(field_name, getattr(self, field_name))
                       for field_name in field_names])
        if url:
            result.update(url=self.get_absolute_url)
        if ref_urls:
            result.update([
                (field_name + '_url',
                 getattr(self, field_name).get_absolute_url())
                for field_name in field_names
                if isinstance(getattr(self, field_name),
                              models.Model)])
        if not ref_objects:
            result.update([
                (field_name, getattr(self, field_name).pk)
                for field_name in field_names
                if isinstance(getattr(self, field_name),
                              models.Model)])
        return result

    def get_absolute_url(self):
        """
        Return absolute url for use in api.

        Convenient when creating manual listviews; djangorestframework does
        so automatically when you use the specialized  ModelResourceView.
        """
        return reverse('lizard_esf_api_' +
                       uncamel(self.__class__.__name__),
                       kwargs={'pk': self.pk})


class NameAbstract(models.Model, GettersMixin):
    """
    Abstract model with only a name as property.
    """
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        abstract = True
        ordering = ['id']

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


class DbfFile(models.Model):
    '''
        DBF file

    '''
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class Configuration(MP_Node):
    """
        ESF configuration.
        Configuration of all objects, for visualisation and export of settings to Fews
    """

    ESF_CHOICES = [(n, n) for n in range(-1, 10)]

    DBF_FIELD_TYPES = (
        ('C', 'Text'),
        ('N', 'Number'),
        ('D', 'Date'),
    )

    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128)
    is_main_esf = models.IntegerField(null=True, choices=ESF_CHOICES,
                                      help_text='esf nummer voor indicatie van hoofd \'stoplichten\'')

    #settings for visualization
    graphgroup_on_expand = models.CharField(max_length=128, null=True, blank=True,
                                     help_text='Grafiek groep die aan gezet moet worden bij openen van dit element')
    source_name = models.CharField(max_length=128,
                                     help_text='Meta data over de Bron waar de automatisch berekende waarde vandaan komt')
    expanded = models.BooleanField(default=False,
                                     help_text='Wordt volgens mij niet meer gebruikt')

    #settings for visualization and editors
    manual = models.NullBooleanField(default=False,
                                     help_text='Kan de eigenschappen worden overruled')
    configuration_type = models.ForeignKey(ConfigurationType,
                                     help_text='Wat voor item is het (resultaat/ instelling/ etc)')
    value_type = models.ForeignKey(ValueType,
                                     help_text='Wat voor type is de waarde. Wordt gebruikt o.a. gebruikt voor editor')

    #settings for getting actual values from Fews
    default_parameter_code_manual_fews = models.CharField(max_length=256,
                                     blank=True,
                                     default='',
                                     help_text='locatie van resultaat in fews met de "<parameter>,<module_instance>\
                                                <timestep>,<qualifier>", gescheiden door comma\' s. Als er bij 1 van\
                                                de eigenschappen niks wordt ingevuld worden alle series geselecteerd en\
                                                de eerste getoond')
    timeserie_ref_status = models.CharField(max_length=256,
                                     blank=True, default='',
                                     help_text='locatie van status (aantal sterren die betrouwbaarheid aangeven) in fews met de \'<parameter>,<module_instance>\
                                                <timestep>,<qualifier>\', gescheiden door comma\'s.) ')

    #settings for export to dbf
    dbf_file = models.ForeignKey(DbfFile, null=True, blank=True,
                                     help_text='Naam van de dbf file voor Fews waarnaar de\
                                                eigenschap geschreven moet worden')
    dbf_index = models.IntegerField(null=True, blank=True, default=0,
                                     help_text='index voor de volgorde van kolommen in de dbf file')
    dbf_valuefield_name = models.CharField(max_length=10,
                                     blank=True,
                                     default='',
                                     help_text='Veldnaam voor de waarde (als leeg, dan wordt de \
                                                eigenschap niet weggeschreven')
    dbf_valuefield_type = models.CharField(max_length=1,
                                           choices=DBF_FIELD_TYPES)
    dbf_valuefield_length = models.IntegerField(null=True, blank=True, default=12,
                                     help_text='lengte van het dbf veld voor de waarde \
                                                eigenschap niet weggeschreven')
    dbf_valuefield_decimals = models.IntegerField(null=True, blank=True,
                                     help_text='Aantal decimalen voor het waarde veld in geval van een number')

    dbf_manualfield_name = models.CharField(max_length=10,
                                     blank=True, default='',
                                     help_text='Veldnaam in dbf voor de eigenschap \'handmatig\'')

    node_order_by = ['code']

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
        The values of the configuration fields for each area.
    """
    area = models.ForeignKey(Area, related_name='esf_areaconfiguration_set')
    configuration = models.ForeignKey(
        Configuration,
        related_name='esf_areaconfiguration_set',
    )
    manual = models.IntegerField(default=0)
    manual_value = models.FloatField(
        blank=True, null=True,
    )
    manual_text_value = models.CharField(max_length=256,
                                         blank=True, null=True)
    comment = models.TextField(max_length=256, blank=True, default='-')
    last_edit_by = models.CharField(max_length=256, blank=True, default='-')
    last_edit_date = models.DateTimeField(auto_now=True)
    last_comment = models.CharField(max_length=256, blank=True, default='-')
    fews_meta_info = models.CharField(max_length=128, null=True, blank=True)

    # Will sometimes give an unicode error.
    # def __unicode__(self):
    #     return '%s %s' % (self.area, self.configuration)

    def get_mydump(self):
        """
        Dump as dict.
        """
        output = {
            'id': self.id,
            'config_id': self.configuration.id,
            'name': self.configuration.name,
            'source_name': self.configuration.source_name,
            'manual': self.manual,
            'manual_value': self.manual_value,
            'manual_text_value': self.manual_text_value,
            'type': self.configuration.value_type.name,
            'is_manual': self.configuration.manual,
            'config_type': self.configuration.configuration_type.name,
            'comment': self.comment,
            'last_edit_by': self.last_edit_by,
            'last_edit_date': self.last_edit_date,
            'iconCls': ('x-tree-custom-%s' %
                        self.configuration.configuration_type.name),  # Icon style class
        }
        if self.configuration.configuration_type.name == 'parameter':
            output['auto_value'] = None
            self.manual = None
        else:
            ts = TimeSeriesCache.objects.filter(
                geolocationcache__ident=self.area.ident,
                parametercache__ident=self.configuration.default_parameter_code_manual_fews)

            if ts.count() > 0:
                try:
                    event = ts[0].get_latest_event()
                    output['auto_value'] = event.value
                    output['auto_value_ts'] = event.timestamp
                except Exception:
                    output['auto_value'] = None
            else:
                output['auto_value'] = None

        return output

    @classmethod
    def dump_tree(cls, area):
        """
        Dump tree of config and children for a specific area as dict.
        """
        def resolve_children(children, choices_dict):
            """
            Resolve the children using elements in choices_dict.

            Children is a list of config-dicts with key 'config_id'
            for each dict.
            """
            for child in children:
                child['children'] = choices_dict.get(child['config_id'], [])
                resolve_children(child['children'], choices_dict)

        area_configs = cls.objects.filter(area=area).order_by(
            'configuration__path')
        config_dict = {}

        # Put all nodes from area_configs into config_dict
        # where the key is the config_id, None is root.
        for area_config in area_configs:
            config_parent = area_config.configuration.get_parent()
            if config_parent:
                parent_id = config_parent.id
            else:
                parent_id = None
            if not parent_id in config_dict:
                config_dict[parent_id] = []
            config_dict[parent_id].append(area_config.get_mydump())

        tree = {'id': -1, 'name': 'root'}
        resolve_children(config_dict[None], config_dict)
        tree['children'] = config_dict[None]

        return tree


def get_auto_value(area, configuration):

    if configuration.configuration_type.name == 'parameter':
        auto_value = None
    else:
        ts = TimeSeriesCache.objects.filter(
            geolocationcache__ident=area.ident,
            parametercache__ident=configuration.default_parameter_code_manual_fews)
        count = ts.count()
        if count > 0:
            if count > 1:
                logger.warning('Found %d time series for %s (expected 0 or 1).',
                    count, configuration.default_parameter_code_manual_fews)
            try:
                event = ts[0].get_latest_event()
                auto_value = event
            except Exception:
                auto_value = None
        else:
            auto_value = None
    return auto_value


def get_data_main_esf(area):
    """
        return major data for the 9 esfs

    """
    configs = AreaConfiguration.objects.filter(
                                    area=area,
                                    configuration__is_main_esf__gt=0
                                ).order_by(
                                    'configuration__is_main_esf')

    #value automatic / value manual
    #date of last calculation / date of last change + naam van persoon die dit heeft ingevoerd
    #de status bepaling + bron (niet beschikbaar)

    data = {}

    for config in configs:
        rec = {}
        rec['name'] = config.configuration.name
        rec['nr'] = config.configuration.is_main_esf
        if config.manual:
            rec['source'] = 'manual'
            rec['value'] = config.manual_value
            rec['source_info'] = config.last_edit_by
            rec['date'] = config.last_edit_date
            rec['stars'] = None
            rec['stars_comment'] = 'expert schatting'
        else:
            auto_value = get_auto_value(area, config.configuration)
            if auto_value is not None:
                rec['source'] = 'auto'
                rec['value'] = auto_value.value
                rec['source_info'] = '' #+ configurationdate?
                rec['date'] = auto_value.timestamp
                rec['stars'] = 0 #auto_status.value
                rec['stars_comment'] = None
            else:
                rec['value'] = 0
                rec['source'] = 'novalue'
                rec['source_info'] = None
                rec['date'] = None
                rec['stars'] = None
                rec['stars_comment'] = 'niet beschikbaar'

        if rec['value'] == 1:
            rec['judgment'] = 'critical'
        elif rec['value'] == 2:
            rec['judgment'] = 'ok'
        else:
            rec['judgment'] = 'novalue'
        #critical
        data[config.configuration.is_main_esf] = rec

    output = []
    for i in range(1,10):
        if i in data:
            output.append(data[i])
        else:
            output.append({
                'judgment': 'novalue',
                'name': i,
                'nr': i,
                'stars_comment': 'niet beschikbaar'
            })

    return output


class DBFConfiguration(models.Model):
    """Configuration to create dbf files."""
    dbf_file = models.ForeignKey(DbfFile)
    data_set = models.ForeignKey(DataSet, null=True, blank=True,
                                 related_name="esf_dbfconfiguration_set")
    save_to = models.CharField(max_length=128, null=True, blank=True,
                               help_text="Example: '/home/naam/dbf/'")
    filename = models.CharField(max_length=128,
                                help_text="Example: 'aanafvoergebieden'")
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s %s" % (self.dbf_file, self.data_set)
