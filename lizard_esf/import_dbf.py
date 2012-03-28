"""
Import WB configurations.
"""
import logging

from dbfpy.dbf import Dbf

from lizard_area.models import Area
from lizard_esf.models import DbfFile
from lizard_esf.models import AreaConfiguration
from lizard_esf.models import Configuration


class DBFImporter(object):
    """
    Import esf configurations from dbf file.
    """

    def __init__(self, logger=None):
        self.fews_meta_info = None
        self.esftype = None
        self.filepath = None
        self.logger = logger
        if self.logger is None:
            self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Run imports for 'esf',

        """
        if self.filepath is None:
            self.logger.warning("Stop validation, file path is None.")
            return
        if self.esftype is None:
            self.logger.warning("Stop validation, esf_type is  None.")
            return

        dbffile = DbfFile.objects.filter(name=self.esftype)
        if dbffile.exists():
            self._import_esfs(dbffile)
        else:
            self.logger.warning("UNKOWN esf type.")

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

    def _update_areaconfigurations(self, area, rec, dbffile, dbffields):
        areaconfigurations = AreaConfiguration.objects.filter(
                configuration__dbf_file=dbffile, area=area)
        self.logger.info(
            "Update esf-configuration of 'aanafvoergebied' '%s'." % area.name)
        amount_updated = 0
        amount_unknown = 0
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
                item.fews_meta_info = self.fews_meta_info
                item.save()
                amount_updated = amount_updated + 1
            else:
                self.logger.info("ESF-configuration '%s' '%s' NOT in dbf." % (
                        dbf_manualfield_name, dbf_valuefield_name)) 
                amount_unknown = amount_unknown + 1
        self.logger.info("'%d' - unknown esf-configurations in dbf." % amount_unknown)         
        self.logger.info("'%d' - updated esf-configurations." % amount_updated)

    def _import_esfs(self, dbffile):
        """Import esfs.
        """
        db = Dbf(self.filepath)
        dbffields = db.fieldNames
        for rec in db:
            ident = rec["GAFIDENT"]
            areas = Area.objects.filter(ident=ident)
            if areas.exists():
                self._create_areaconfigurations(areas[0], dbffile)
            else:
                self.logger.warning(
                    "Aanafvoergebied ident='%s' does not exist." % ident)
                continue

            self._update_areaconfigurations(areas[0], rec, dbffile, dbffields)
        db.close()
