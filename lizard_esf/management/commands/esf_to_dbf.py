#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.core.management.base import BaseCommand
from lizard_esf.models import DBFConfiguration
from lizard_esf.dbf_utils import export_esf_configurations

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Exports 'esf into dbf file.
    """

    help = ("Example: bin/django esf_to_dbf")

    def handle(self, *args, **options):
        self.export()

    def export(self):
        dbf_configurations = DBFConfiguration.objects.filter(enabled=True)
        logger.info("%s esf configurations to export." % len(
                dbf_configurations))
        for dbf_configuration in dbf_configurations:
            owner = dbf_configuration.data_set
            save_to = dbf_configuration.save_to
            dbf_file = dbf_configuration.dbf_file
            filename = dbf_configuration.filename
            export_esf_configurations(owner, save_to, dbf_file, filename)
        logger.info("Export of esf configurations is finished.")
