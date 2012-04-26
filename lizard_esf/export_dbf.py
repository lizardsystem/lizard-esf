"""
DBF utils to create dbf files.
"""
import os

from lizard_esf.models import AreaConfiguration
from lizard_esf.models import Configuration
from lizard_esf.models import DbfFile

from lizard_area.models import Area

from dbfpy.dbf import Dbf

import logging


class DBFExporter(object):
    """
    Creates a dbf file.
    """

    def __init__(self, logger=None):
        if logger is not None:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)

    def export_esf_configurations(self, owner, save_to, dbf_file, filename):
        """Export esf configurations into dbf.

        Arguments:
        owner -- instance of lizard_security DataSet object
        save_to -- location to save dbf file as string, ex. '/tmp/'
        dbf_file -- instance of DbfFile object
        """
        if owner is not None:
            areas = Area.objects.filter(data_set=owner)
        else:
            areas = Area.objects.exclude(data_set=None)
        areas = areas.exclude(area_class=Area.AREA_CLASS_KRW_WATERLICHAAM)

        configurations = Configuration.objects.filter(
            dbf_file=dbf_file).order_by('dbf_index')
        if configurations.exists() == False:
            self.logger.warning('NO configurations for dbf_file %s' % dbf_file)
            return

        filepath = self.file_path(save_to, filename, 'dbf')
        if filepath is None:
            self.logger.error("File path='%s' does NOT exist." % save_to)
            return

        self.logger.debug("Creating dbf file: %s." % filepath)

        self.create_out(filepath)

        self.fields_to_dbf(configurations)

        counter = 0
        for area in areas:
            areaconfigurations = AreaConfiguration.objects.filter(
                configuration__dbf_file=dbf_file,
                area=area)
            counter = counter + len(areaconfigurations)
            if areaconfigurations.exists():
                self.store_data(area, areaconfigurations)
        self.logger.debug("Processed %d areaconfigurations." % counter)

        self.close_out()

    def field_to_dbf(
        self, f_name, f_type, f_length=None, f_decimals=None):
        """Add a field into passed dbf.

        Arguments:
        f_name -- field name as string where len(f_name)<= 10
        f_type -- field type as string (C, D, N)
        f_length -- decimals as integer
        """
        field_options = [f_name, f_type]
        if f_length is not None:
            field_options.append(f_length)
        if f_length is not None and f_decimals is not None:
            field_options.append(f_decimals)
        try:
            self.add_field_out(field_options)
        except Exception as ex:
            self.logger.error(','.join(map(str, ex.args)))

    def fields_to_dbf(self, mapping):
        """
        Add fields into dbf file.
        Avoid fields with None or empty value.
        """
        self.field_to_dbf(u'GAF_ID', 'N', 9, 0)
        self.field_to_dbf(u'GAFIDENT', 'C', 24)
        self.field_to_dbf(u'GAFNAME', 'C', 100)
        for item in mapping:
            if self.is_nonempty_value(item.dbf_valuefield_name):
                self.field_to_dbf(item.dbf_valuefield_name,
                                  item.dbf_valuefield_type,
                                  item.dbf_valuefield_length,
                                  item.dbf_valuefield_decimals)
            if self.is_nonempty_value(item.dbf_manualfield_name):
                self.field_to_dbf(item.dbf_manualfield_name, 'L')

    def store_data(self, area, areaconfigurations):
        """
        Store data into dbf file.
        """
        rec = self.new_record()
        rec['GAF_ID'] = area.id
        rec['GAFIDENT'] = area.ident
        rec['GAFNAME'] = area.name

        for item in areaconfigurations:

            dbf_manualfield_name = item.configuration.dbf_manualfield_name
            dbf_valuefield_name = item.configuration.dbf_valuefield_name

            manual_text_value = item.manual_text_value
            manual_value = item.manual_value
            value = item.manual

            if self.is_nonempty_value(dbf_manualfield_name) and \
                self.is_nonempty_value(value):
                rec[dbf_manualfield_name] = value

            if self.is_nonempty_value(dbf_valuefield_name):
                if item.configuration.dbf_valuefield_type == 'C':
                    if self.is_nonempty_value(manual_text_value):
                        rec[dbf_valuefield_name] = manual_text_value
                else:
                    if self.is_nonempty_value(manual_value):
                        if item.configuration.dbf_valuefield_type == 'L':
                            manual_value = manual_value > 0.0
                        rec[dbf_valuefield_name] = manual_value

        self.store_record(rec)

    def file_path(self, save_to, filename, extension):
        """
        Create absolute filepath.

        Arguments:
        save_to -- pathname as string, example. '/tmp/share/'
        filename -- filename as string, example. 'aanafvoergebied'
        extention -- file extention as string, example. 'dbf'
        """
        success = True
        if not os.path.exists(save_to):
            self.logger.error("Path %s not exists" % save_to)
            success = False

        if filename is None or len(filename) < 1:
            self.logger.error("File name is not exists")
            success = False

        if success:
            filename = ".".join((filename, extension))
            filepath = os.path.abspath(os.path.join(save_to, filename))
        else:
            filepath = None
        return filepath

    def is_nonempty_value(self, value):
        return ((value is not None) and (value != ''))

    def create_out(self, file_path):
        self.out = Dbf(file_path, new=True)

    def add_field_out(self, field_options):
        self.out.addField(tuple(field_options))

    def close_out(self):
        self.out.close()

    def new_record(self):
        return self.out.newRecord()

    def store_record(self, rec):
        rec.store()


class DBFExporterToDict(DBFExporter):
    """Implements the export of a DBF to a dictionary."""

    def __init__(self, *args, **kwargs):
        DBFExporter.__init__(self, *args, **kwargs)

    def file_path(self, save_to, filename, extension):
        return "don't care"

    def create_out(self, file_path):
        self.out = []

    def add_field_out(self, field_options):
        pass

    def close_out(self):
        pass

    def new_record(self):
        return {}

    def store_record(self, rec):
        self.out.append(rec)

class ESFRecords(object):

    def retrieve_records(self, config):
        """Return the list of records from the given configuration.

        Each record is specified as a dict from attribute name to attribute
        value.

        """
        exporter = DBFExporterToDict()
        dbf_file = DbfFile.objects.get(name=config.config_type)
        exporter.export_esf_configurations(config.data_set, "don't care",
            dbf_file, "don't care")
        return exporter.out
