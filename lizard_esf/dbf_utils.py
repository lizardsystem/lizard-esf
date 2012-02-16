"""
DBF utils to create dbf files.
"""
import os

from lizard_esf.models import AreaConfiguration
from lizard_esf.models import Configuration

from lizard_area.models import Area

from dbfpy.dbf import Dbf

import logging
logger = logging.getLogger(__name__)


def file_path(save_to, filename, extention):
    """
    Create absolute filepath.

    Arguments:
    save_to -- pathname as string, example. '/tmp/share/'
    filename -- filename as string, example. 'aanafvoergebied'
    extention -- file extention as string, example. 'dbf'
    """
    success = True
    if not os.path.exists(save_to):
        logger.error("Path %s not exists" % save_to)
        success = False

    if filename is None or len(filename) < 1:
        logger.error("File name is not exists")
        success = False

    if success:
        filename = ".".join((filename, extention))
        filepath = os.path.abspath(os.path.join(save_to, filename))
    else:
        filepath = None
    return filepath


def field_to_dbf(out, f_name, f_type, f_length=None, f_decimals=None):
    """Add a field into passed dbf.

    Arguments:
    out -- instance of DBF file
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
        out.addField(tuple(field_options))
    except Exception as ex:
        logger.error(','.join(map(str, ex.args)))


def fields_to_dbf(mapping, out):
    """
    Adds fields into dbf file.
    """
    field_to_dbf(out, 'GAF_ID', 'N', 9, 0)
    field_to_dbf(out, 'GAFIDENT', 'C', 24)
    field_to_dbf(out, 'GAFNAME', 'C', 100)
    for item in mapping:
        field_to_dbf(out,
                     item.dbf_valuefield_name,
                     item.dbf_valuefield_type,
                     item.dbf_valuefield_length,
                     item.dbf_valuefield_decimals)

        field_to_dbf(out,
                     item.dbf_manualfield_name,
                     item.dbf_valuefield_type,
                     item.dbf_valuefield_length,
                     item.dbf_valuefield_decimals)


def store_data(out, area, areaconfigurations):
    """
    Store data into dbf file.
    """
    rec = out.newRecord()
    rec['GAF_ID'] = area.id
    rec['GAFIDENT'] = area.ident
    rec['GAFNAME'] = area.name

    for item in areaconfigurations:

        dbf_manualfield_name = item.configuration.dbf_manualfield_name
        dbf_valuefield_name = item.configuration.dbf_valuefield_name

        manual_value = item.manual_value
        value = item.manual
        print "%s | %s" % (value, manual_value)

        if dbf_manualfield_name is not None and manual_value is not None:
            rec[dbf_manualfield_name] = manual_value

        if dbf_valuefield_name is not None and value is not None:
            rec[dbf_valuefield_name] = value
    rec.store()


def export_esf_configurations(owner, save_to, dbf_file, filename):
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
        logger.debug('NO configurations for dbf_file %s' % dbf_file)
        return

    filepath = file_path(save_to, filename, 'dbf')
    if filepath is None:
        logger.error("File path='%s' does NOT exist." % save_to)
        return

    logger.debug("Creating dbf file: %s." % filepath)
    out = Dbf(filepath, new=True)

    fields_to_dbf(configurations, out)

    counter = 0
    for area in areas:
        areaconfigurations = AreaConfiguration.objects.filter(
            configuration__dbf_file=dbf_file,
            area=area)
        counter = counter + len(areaconfigurations)
        if areaconfigurations.exists():
            store_data(out, area, areaconfigurations)
    logger.debug("Processed %d areaconfigurations." % counter)
    out.close()
