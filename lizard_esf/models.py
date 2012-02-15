# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import re

from django.core.urlresolvers import reverse
from django.db import models

from lizard_area.models import Area
from treebeard.mp_tree import MP_Node
from lizard_fewsnorm.models import TimeSeriesCache

# from django.core.urlresolvers import reverse
# from lizard_fewsnorm.models import TimeseriesKeys


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
    """

    DBF_FIELD_TYPES = (
        ('C', 'Text'),
        ('N', 'Number'),
        ('D', 'Date'),
    )


    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128)
    source_name = models.CharField(max_length=128)#bron
    expanded = models.BooleanField(default=False)

    configuration_type = models.ForeignKey(ConfigurationType)#setting/ uitkomst/ ?????
    value_type = models.ForeignKey(ValueType)#number, boolean, oordeel

    default_parameter_code_manual_fews = models.CharField(max_length=256, blank=True, default='')
    #format: parametercode,moduleinstance_code,timestep_code met een comma ertussen
    # uitkomst in fews
    timeserie_ref_status = models.CharField(max_length=256, blank=True, default='')#betrouwbaarheid
    #format: parametercode,moduleinstance_code,timestep_code met een comma ertussen

    manual = models.NullBooleanField(default=False) #overrulen

    dbf_file = models.ForeignKey(DbfFile, null=True, blank=True)
    dbf_index = models.IntegerField(null=True, blank=True)

    dbf_valuefield_name = models.CharField(max_length=128, blank=True, default='')
    dbf_valuefield_type = models.CharField(max_length=1, choices=DBF_FIELD_TYPES)
    dbf_valuefield_length = models.IntegerField(null=True, blank=True)
    dbf_valuefield_decimals = models.IntegerField(null=True, blank=True)

    dbf_manualfield_name = models.CharField(max_length=128, blank=True, default='') #fixed format

    node_order_by = ['name']

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
    comment = models.TextField(max_length=256, blank=True, default='-')
    last_edit_by = models.CharField(max_length=256, blank=True, default='-')
    last_edit_date = models.DateTimeField(auto_now=True)
    last_comment = models.CharField(max_length=256, blank=True, default='-')

    def get_mydump(self):

        output = {
            'id': self.id,
            'config_id': self.configuration.id,
            'name': self.configuration.name,
            'source_name': self.configuration.source_name,
            'manual': self.manual,
            'manual_value': self.manual_value,
            'type': self.configuration.value_type.name,
            'is_manual': self.configuration.manual,
            'config_type': self.configuration.configuration_type.name,
            'last_comment': 'ja ja ja',
        }
        if self.configuration.configuration_type.name == 'parameter':
            output['auto_value'] = None
            self.manual = None
        else:
            ts = TimeSeriesCache.objects.filter(geolocationcache__ident=self.area.ident, parametercache__ident=self.configuration.default_parameter_code_automatic_fews)
            #self.area.ident
            print ts.count()
            if ts.count() > 0:
                try:
                    event = ts[0].get_latest_event()

                    output['auto_value'] = event.value
                    output['auto_value_ts'] = event.timestamp
                except Exception, e:
                    print 'error: '
                    print e
                    output['auto_value'] =  None

            else:

                output['auto_value'] =  None


        return output


def tree(config):
    a = {}
    for b in config:
        if b.configuration.get_parent():
            parent_id = b.configuration.get_parent().id
        else:
            parent_id = None
            pass
        config_id = b.configuration.id

        if not parent_id in a:
            a[parent_id] = []
        if not config_id in a:
            a[config_id] = []
        a[parent_id].append(b.get_mydump())

    tree = {'id': -1, 'name': 'root'}

    tree['children'] = a[None]

    for child in tree['children']:

        child['children'] = a[child['config_id']]

        for child_1 in child['children']:
            child_1['children'] = a[child_1['config_id']]

            for child_2 in child_1['children']:
                child_2['children'] = a[child_2['config_id']]

                for child_3 in child_2['children']:
                    child_3['children'] = a[child_3['config_id']]

    return tree
