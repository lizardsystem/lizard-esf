Changelog of lizard-esf
===================================================


0.17 (unreleased)
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
