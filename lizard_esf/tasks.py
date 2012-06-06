#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) 2012 Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

import logging

from celery.task import task

from lizard_esf.import_dbf import DBFImporter
from lizard_esf.models import DBFConfiguration
from lizard_esf.export_dbf import DBFExporter
from lizard_esf.models import DbfFile

from lizard_task.task import task_logging


def get_logger(handler, taskname, levelno):
    """Create logger to log messages into db."""
    logger = logging.getLogger(taskname)
    logger.addHandler(handler)
    logger.setLevel(int(levelno))
    return logger


@task()
@task_logging
def import_dbf_all(taskname="",
                   data_set=None,
                   username=None,
                   levelno=20):
    """
    Import esf configurations from dbf.
    """
    logger = logging.getLogger(taskname)
    dbffiles = DbfFile.objects.all()
    for dbffile in dbffiles:
        dbfimporter = DBFImporter(logger)
        dbfimporter.esftype = dbffile.name
        dbfimporter.data_set = data_set
        logger.info("Start import of '%s'." % dbffile.name)
        dbfimporter.run()
    logger.info("END IMPORT.")


@task()
@task_logging
def import_dbf(taskname="",
               username=None,
               levelno=20,
               data_set=None,
               esftype=None):
    """
    Import esf configurations from dbf.
    """
    logger = logging.getLogger(taskname)
    dbfimporter = DBFImporter(logger)
    dbfimporter.esftype = esftype
    dbfimporter.data_set = data_set
    logger.info("Start import of '%s'." % esftype)
    dbfimporter.run()
    logger.info("END IMPORT.")


@task()
@task_logging
def export_esf_to_dbf(
    data_set=None,
    levelno=20,
    username=None,
    taskname=""):
    """
    Export esf configurations into dbf.
    """
    logger = logging.getLogger(taskname)
    dbfexporter = DBFExporter(logger)
    dbf_configurations = DBFConfiguration.objects.filter(enabled=True)
    if data_set is not None:
        dbf_configurations = dbf_configurations.filter(data_set__name=data_set)
    logger.info("%s esf configurations to export." % len(
            dbf_configurations))
    for dbf_configuration in dbf_configurations:
        owner = dbf_configuration.data_set
        save_to = dbf_configuration.save_to
        dbf_file = dbf_configuration.dbf_file
        filename = dbf_configuration.filename
        logger.info("Start export '%s' for '%s'." % (dbf_file, owner))
        dbfexporter.export_esf_configurations(
            owner, save_to, dbf_file, filename)
        logger.info("End export '%s' for '%s'." % (dbf_file, owner))
    logger.info("END EXPORT.")


def run_export_esf_to_dbf():
    """Run export_esf_to_dbf task for HHNK as test."""
    kwargs = {"data_set": "HHNK"}
    export_esf_to_dbf.delay(**kwargs)


def run_importdbf_task():
    """Run import_dbf task as test."""
    kwargs = {'esftype': 'esf1',
              'taskname': 'esf_import_dbf_waternet',
              'username': 'admin',
              'levelno': 20,
              'data_set': 'Waternet'}
    import_dbf.delay(**kwargs)
