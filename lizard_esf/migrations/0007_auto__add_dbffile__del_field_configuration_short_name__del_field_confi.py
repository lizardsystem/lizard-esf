# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DbfFile'
        db.create_table('lizard_esf_dbffile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('lizard_esf', ['DbfFile'])

        # Deleting field 'Configuration.short_name'
        db.delete_column('lizard_esf_configuration', 'short_name')

        # Deleting field 'Configuration.default_parameter_code_automatic_fews'
        db.delete_column('lizard_esf_configuration', 'default_parameter_code_automatic_fews')

        # Deleting field 'Configuration.default_parameter_code_final_fews'
        db.delete_column('lizard_esf_configuration', 'default_parameter_code_final_fews')

        # Adding field 'Configuration.timeserie_ref_status'
        db.add_column('lizard_esf_configuration', 'timeserie_ref_status', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True), keep_default=False)

        # Adding field 'Configuration.dbf_file'
        db.add_column('lizard_esf_configuration', 'dbf_file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_esf.DbfFile'], null=True, blank=True), keep_default=False)

        # Adding field 'Configuration.dbf_index'
        db.add_column('lizard_esf_configuration', 'dbf_index', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Configuration.dbf_valuefield_name'
        db.add_column('lizard_esf_configuration', 'dbf_valuefield_name', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True), keep_default=False)

        # Adding field 'Configuration.dbf_valuefield_type'
        db.add_column('lizard_esf_configuration', 'dbf_valuefield_type', self.gf('django.db.models.fields.CharField')(default='C', max_length=1), keep_default=False)

        # Adding field 'Configuration.dbf_valuefield_length'
        db.add_column('lizard_esf_configuration', 'dbf_valuefield_length', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Configuration.dbf_valuefield_decimals'
        db.add_column('lizard_esf_configuration', 'dbf_valuefield_decimals', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Configuration.dbf_manualfield_name'
        db.add_column('lizard_esf_configuration', 'dbf_manualfield_name', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True), keep_default=False)

        # Changing field 'Configuration.default_parameter_code_manual_fews'
        db.alter_column('lizard_esf_configuration', 'default_parameter_code_manual_fews', self.gf('django.db.models.fields.CharField')(max_length=256))

        # Adding field 'AreaConfiguration.comment'
        db.add_column('lizard_esf_areaconfiguration', 'comment', self.gf('django.db.models.fields.TextField')(default='-', max_length=256, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'DbfFile'
        db.delete_table('lizard_esf_dbffile')

        # Adding field 'Configuration.short_name'
        db.add_column('lizard_esf_configuration', 'short_name', self.gf('django.db.models.fields.CharField')(default='-', max_length=128), keep_default=False)

        # Adding field 'Configuration.default_parameter_code_automatic_fews'
        db.add_column('lizard_esf_configuration', 'default_parameter_code_automatic_fews', self.gf('django.db.models.fields.CharField')(default='-', max_length=128), keep_default=False)

        # Adding field 'Configuration.default_parameter_code_final_fews'
        db.add_column('lizard_esf_configuration', 'default_parameter_code_final_fews', self.gf('django.db.models.fields.CharField')(default='-', max_length=128), keep_default=False)

        # Deleting field 'Configuration.timeserie_ref_status'
        db.delete_column('lizard_esf_configuration', 'timeserie_ref_status')

        # Deleting field 'Configuration.dbf_file'
        db.delete_column('lizard_esf_configuration', 'dbf_file_id')

        # Deleting field 'Configuration.dbf_index'
        db.delete_column('lizard_esf_configuration', 'dbf_index')

        # Deleting field 'Configuration.dbf_valuefield_name'
        db.delete_column('lizard_esf_configuration', 'dbf_valuefield_name')

        # Deleting field 'Configuration.dbf_valuefield_type'
        db.delete_column('lizard_esf_configuration', 'dbf_valuefield_type')

        # Deleting field 'Configuration.dbf_valuefield_length'
        db.delete_column('lizard_esf_configuration', 'dbf_valuefield_length')

        # Deleting field 'Configuration.dbf_valuefield_decimals'
        db.delete_column('lizard_esf_configuration', 'dbf_valuefield_decimals')

        # Deleting field 'Configuration.dbf_manualfield_name'
        db.delete_column('lizard_esf_configuration', 'dbf_manualfield_name')

        # Changing field 'Configuration.default_parameter_code_manual_fews'
        db.alter_column('lizard_esf_configuration', 'default_parameter_code_manual_fews', self.gf('django.db.models.fields.CharField')(max_length=128))

        # Deleting field 'AreaConfiguration.comment'
        db.delete_column('lizard_esf_areaconfiguration', 'comment')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lizard_area.area': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Area', '_ormbases': ['lizard_area.Communique']},
            'area_class': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'area_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'communique_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_area.Communique']", 'unique': 'True', 'primary_key': 'True'}),
            'data_administrator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.DataAdministrator']", 'null': 'True', 'blank': 'True'}),
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_security.DataSet']", 'null': 'True', 'blank': 'True'}),
            'dt_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 2, 14, 11, 30, 32, 91540)'}),
            'dt_latestchanged': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dt_latestsynchronized': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Area']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_area.communique': {
            'Meta': {'object_name': 'Communique', '_ormbases': ['lizard_geo.GeoObject']},
            'areasort': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'areasort_krw': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'dt_latestchanged_krw': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'edited_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'edited_by': ('django.db.models.fields.TextField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'geoobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_geo.GeoObject']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'surface': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'watertype_krw': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'lizard_area.dataadministrator': {
            'Meta': {'object_name': 'DataAdministrator'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_esf.areaconfiguration': {
            'Meta': {'object_name': 'AreaConfiguration'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'esf_areaconfiguration_set'", 'to': "orm['lizard_area.Area']"}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "'-'", 'max_length': '256', 'blank': 'True'}),
            'configuration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'esf_areaconfiguration_set'", 'to': "orm['lizard_esf.Configuration']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_comment': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '256', 'blank': 'True'}),
            'last_edit_by': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '256', 'blank': 'True'}),
            'last_edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'manual': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'manual_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'lizard_esf.configuration': {
            'Meta': {'object_name': 'Configuration'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'configuration_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_esf.ConfigurationType']"}),
            'dbf_file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_esf.DbfFile']", 'null': 'True', 'blank': 'True'}),
            'dbf_index': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dbf_manualfield_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'dbf_valuefield_decimals': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dbf_valuefield_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dbf_valuefield_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'dbf_valuefield_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'default_parameter_code_manual_fews': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'expanded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'source_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timeserie_ref_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'value_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_esf.ValueType']"})
        },
        'lizard_esf.configurationtype': {
            'Meta': {'ordering': "['id']", 'object_name': 'ConfigurationType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_esf.dbffile': {
            'Meta': {'object_name': 'DbfFile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'lizard_esf.valuetype': {
            'Meta': {'ordering': "['id']", 'object_name': 'ValueType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_geo.geoobject': {
            'Meta': {'object_name': 'GeoObject'},
            'geo_object_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_geo.GeoObjectGroup']"}),
            'geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'lizard_geo.geoobjectgroup': {
            'Meta': {'object_name': 'GeoObjectGroup'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'source_log': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'lizard_security.dataset': {
            'Meta': {'ordering': "['name']", 'object_name': 'DataSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        }
    }

    complete_apps = ['lizard_esf']
