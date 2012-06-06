Changelog of lizard-esf
===================================================


0.26.2 (2012-06-06)
-------------------

- Put edit_message from request on object when saving.
  For lizard_history summary.


0.26.1 (2012-06-06)
-------------------

- Bring summary column back for esf history.


0.26 (2012-06-06)
-----------------

- fix for histlory page in ie

0.25 (2012-05-31)
-----------------

- Improved esf auto_value checking by adding "is not None".

- Added task 'import_dbf_all' to import all esftypes at once.

- Added functionality to remove rejected configuration on validation.

- Improved logging of celery tasks.


0.24 (2012-05-30)
-----------------

- changed look and feel esf-overview


0.23 (2012-05-29)
-----------------

- fix in values for ESF overview (pp 325)


0.22 (2012-05-29)
-----------------

- Add urls and views for history of esf configuration.

- Add template for extjs component for esf tree history.

- Fix area not displaying in history form.

- Main esf overview and editor


0.21 (2012-05-09)
-----------------

- Fixes the spelling of the 'GAFNAAM' DBF column (which was spelled as
  'GAFNAME').


0.20 (2012-05-08)
-----------------

- Adds functionality to export an ESF configuration to a list instead of a DBF
  file (required to compute a diff of a new and an existing ESF configuration).


0.19 (2012-04-26)
-----------------

- Added migration schema.


0.18 (2012-04-26)
-----------------

- Added functionality to retrieve data from fews database
  by related location id for esf-configurations. To use it
  fill 'related_location' field of Configuration model in
  django admin interface.


0.17 (2012-04-19)
-----------------

- Bugfix esf overview: it now works for auto values. Removed "double
  implementation" of same functionality.


0.16 (2012-04-19)
-----------------

- Adds a check to correct the output of logical fields to dbf.


0.15 (2012-04-18)
-----------------

- Shows the Path and Depth values again in the admin screen for
  Configuration(s).

- Added 'L'(logical) option to 'dbf_value_type' field in Configuration model.


0.14 (2012-04-16)
-----------------

- Fixed an error in the import of ESF configurations.


0.13.1 (2012-04-15)
-------------------

- missing migration


0.13 (2012-04-15)
-----------------

- changed icons in tree

- fixed saving and loading of text values in tree

- added overwriteble setting fields (expert_setting)


0.12 (2012-04-11)
-----------------

- Added functionality to import esf-configurations from dbf.

- Changed the way to retrieve a filepath of dbf.


0.11 (2012-04-10)
-----------------

- Added functionality to export esf-configurations to dbf.

- Implemented functionality to parse value of Configuration.default_parameter_code_manual_fews field.


0.10.1 (2012-04-03)
-------------------

- Removed __unicode__ from AreaConfiguration: it will sometimes give
  an error.


0.10 (2012-04-03)
-----------------

- Added iconCls to esf configuration.

- Modernized ESF tree calculation.


0.9 (2012-03-28)
----------------

- Corrects the retrieval of ESF information of an area


0.8 (2012-03-16)
----------------

- Added extra fields to Configuration model.

- Configured testsettings.


0.7 (2012-02-23)
----------------

- Removed fixture lizard_esf.


0.6 (2012-02-23)
----------------

- Added functionality to export esf configurations into dbf.

- Created fixture.


0.5 (2012-02-02)
----------------

- Made get latest value from Fews function area sensitive (instaead of dummy value)


0.4 (2011-12-27)
----------------

- Field manual can now be null as well

- Adds basic security - all operations are now forbidden when not
  authenticated


0.3 (2011-12-09)
----------------

- Nothing changed yet.


0.2 (2011-12-07)
----------------

- Replaced ModelResources in api by custom views.

- Adds form for the name-only models

- Adds post possibility in root views of -type models

- Adds admin for all models


0.1 (2011-11-07)
----------------

- Initial library skeleton created by nensskel.  [your name]

- Initial models and views. Works in Chrome.
