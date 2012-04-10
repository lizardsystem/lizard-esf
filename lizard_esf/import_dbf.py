"""
Import WB configurations.
"""
import logging

from dbfpy.dbf import Dbf

from lizard_esf.models import DbfFile
from lizard_esf.models import AreaConfiguration
from lizard_esf.models import Configuration

from lizard_portal.models import ConfigurationToValidate


class DBFImporter(object):
    """
    Import esf configurations from dbf file.

    class parameters:
    data_set -- name of data_set as string
    esftype -- type of esf file as string, f.e. 'esf1', 'esf2'
    logger -- instance of logging logger
    action -- action of ConfigurationToValidate as number,
    1 = validate
    """

    def __init__(self, logger=None):
        self.data_set = ""
        self.esftype = ""
        self.logger = logger
        self.action = 1
        if self.logger is None:
            self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Run imports for 'esf'.

        """
        if self.esftype == "":
            self.logger.warning(
                "Stop validation, esf_type is an empty string.")
            return
        v_configs = self._configurations()
        if v_configs.exists() == False:
            self.logger.warning(
                "No valid configuration to import for '%s', '%s'." % (
                self.data_set, self.esftype))
            return
        v_configs = v_configs.order_by("file_path")
        esftype_objects = DbfFile.objects.filter(name=self.esftype)
        if esftype_objects.exists():
            for v_config in v_configs:
                dbf_instance = self._open_dbf(v_config.file_path)
                status_tuple = self._import_esfs(
                    dbf_instance, v_config, esftype_objects[0])
                self.validation_status(status_tuple, v_config)
                if dbf_instance is not None:
                    dbf_instance.close()
        else:
            self.logger.warning("UNKOWN esf type.")

    def validation_status(self, status_tuple, v_config):
        """Remove validation object on success or change
        the status to KEEP on error.

        Arguments:
        status_tuple - tuple containing status and error message
        v_config - instance of ConfigurationToValidate model
        """

        msg = "UNKNOWN update status='%s'." % str(status_tuple)[:200]
        if isinstance(status_tuple, tuple) == False:
            self.logger.warning(msg)
            v_config.action_log = msg
            v_config.save()
            return

        if len(status_tuple) < 2:
            self.logger.warning(msg)
            v_config.action_log = msg
            v_config.save()
            return

        status = int(status_tuple[0])
        msg = status_tuple[1][:256]

        if status == 1:
            ConfigurationToValidate.objects.get(id=v_config.id).delete()
        else:
            v_config.action_log = msg
            v_config.action = status
            v_config.save()

    def _configurations(self):
        """Return configurations to validate."""
        configs = ConfigurationToValidate.objects.filter(
            data_set__name=self.data_set,
            config_type=self.esftype,
            action=self.action)
        configs = configs.exclude(file_path=None)
        return configs

    def _create_areaconfigurations(self, area, dbffile):
        """Create not existing areaconfigurations."""

        configs = Configuration.objects.exclude(
            esf_areaconfiguration_set__area=area)
        configs = configs.filter(dbf_file=dbffile)
        self.logger.info(
            "Create %s new esf-configurations." % len(configs))
        for config in configs:
            AreaConfiguration.objects.get_or_create(
                configuration=config, area=area)

    def _update_areaconfigurations(self, v_config, rec, dbffile, dbffields):
        """Update esf-configuration with data from passed dbf-record

        Arguments:
        v_config"""
        areaconfigurations = AreaConfiguration.objects.filter(
                configuration__dbf_file=dbffile, area=v_config.area)
        self.logger.info(
            "Update esf-configuration of 'aanafvoergebied' '%s'." % (
                v_config.area.name))
        amount_updated = 0
        for item in areaconfigurations:
            dbf_manualfield_name = item.configuration.dbf_manualfield_name
            dbf_valuefield_name = item.configuration.dbf_valuefield_name
            updated = False
            if dbf_manualfield_name in dbffields:
                item.manual = rec[dbf_manualfield_name]
                updated = True
            if dbf_valuefield_name in dbffields:
                if isinstance(rec[dbf_valuefield_name], str):
                    item.manual_text_value = rec[dbf_valuefield_name]
                else:
                    item.manual_value = rec[dbf_valuefield_name]
                updated = True
            if updated:
                item.fews_meta_info = v_config.fews_meta_info
                try:
                    item.save()
                    amount_updated = amount_updated + 1
                except Exception as ex:
                    msg = ",".join(map(str, ex.args))
                    self.logger.error(msg)
                    return (False, "Error on update '%s', '%s': %s." % (
                            dbf_manualfield_name,
                            dbf_valuefield_name, msg[:100]))
            else:
                msg = "ESF-configuration '%s' '%s' NOT in dbf." % (
                        dbf_manualfield_name, dbf_valuefield_name)
                self.logger.error(msg)
                return (False, msg)
        self.logger.info("'%d' - updated esf-configurations." % amount_updated)
        return (True, "")

    def _open_dbf(self, filepath):
        """Return instance of dbf file."""
        dbf = None
        try:
            dbf = Dbf(filepath)
        except Exception as ex:
            self.logger.error(','.join(map(str, ex.args)))
        return dbf

    def _set_import_status(v_config, status_msg):
        """Set status to validated object.

        Arguments:
        v_config -- instance of ConfigurationToValidate object
        status_msg -- status as string, free choice
        """
        v_config.status = status_msg
        v_config.save()

    def _import_esfs(self, dbf_instance, v_config, esftype_objects):
        """Import esfs and return a status as tuple object.
        TODO - save results, create areaconfigurations per area.
        """
        status_tuple = None

        if dbf_instance is None:
            return

        dbffields = dbf_instance.fieldNames
        for rec in dbf_instance:
            ident = rec["GAFIDENT"]
            if v_config.area.ident.lower() == ident.lower():
                self._create_areaconfigurations(v_config.area, esftype_objects)
                status_tuple = self._update_areaconfigurations(
                    v_config, rec, esftype_objects, dbffields)
                return status_tuple

        msg = "Aanafvoergebied ident='%s' is not in dbf='%s'." % (
            v_config.area.ident, v_config.file_path)
        self.logger.warning(msg)
        return (False, msg)
