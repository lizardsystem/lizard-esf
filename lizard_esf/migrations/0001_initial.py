# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ConfigurationType'
        db.create_table('lizard_esf_configurationtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal('lizard_esf', ['ConfigurationType'])

        # Adding model 'ValueType'
        db.create_table('lizard_esf_valuetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal('lizard_esf', ['ValueType'])

        # Adding model 'Configuration'
        db.create_table('lizard_esf_configuration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('numchild', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('source_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('configuration_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_esf.ConfigurationType'])),
            ('default_parameter_code_manual_fews', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('default_parameter_code_automatic_fews', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('default_parameter_code_final_fews', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('value_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_esf.ValueType'])),
            ('expanded', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('lizard_esf', ['Configuration'])

        # Adding model 'AreaConfiguration'
        db.create_table('lizard_esf_areaconfiguration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(related_name='esf_areaconfiguration_set', to=orm['lizard_area.Area'])),
            ('configuration', self.gf('django.db.models.fields.related.ForeignKey')(related_name='esf_areaconfiguration_set', to=orm['lizard_esf.Configuration'])),
            ('manual', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('manual_value', self.gf('django.db.models.fields.DecimalField')(default=-999, max_digits=15, decimal_places=1)),
            ('last_edit_by', self.gf('django.db.models.fields.CharField')(default='-', max_length=256, blank=True)),
            ('last_edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_comment', self.gf('django.db.models.fields.CharField')(default='-', max_length=256, blank=True)),
        ))
        db.send_create_signal('lizard_esf', ['AreaConfiguration'])


    def backwards(self, orm):
        
        # Deleting model 'ConfigurationType'
        db.delete_table('lizard_esf_configurationtype')

        # Deleting model 'ValueType'
        db.delete_table('lizard_esf_valuetype')

        # Deleting model 'Configuration'
        db.delete_table('lizard_esf_configuration')

        # Deleting model 'AreaConfiguration'
        db.delete_table('lizard_esf_areaconfiguration')


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
            'communique_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_area.Communique']", 'unique': 'True', 'primary_key': 'True'}),
            'data_administrator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.DataAdministrator']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Area']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_area.areacode': {
            'Meta': {'object_name': 'AreaCode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.areatype': {
            'Meta': {'object_name': 'AreaType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.basin': {
            'Meta': {'object_name': 'Basin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.communique': {
            'Meta': {'object_name': 'Communique', '_ormbases': ['lizard_geo.GeoObject']},
            'area_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.AreaType']", 'null': 'True', 'blank': 'True'}),
            'basin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Basin']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.AreaCode']", 'null': 'True', 'blank': 'True'}),
            'geoobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_geo.GeoObject']", 'unique': 'True', 'primary_key': 'True'}),
            'municipality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Municipality']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Province']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Status']", 'null': 'True', 'blank': 'True'}),
            'watermanagementarea': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.WaterManagementArea']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_area.dataadministrator': {
            'Meta': {'object_name': 'DataAdministrator'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.municipality': {
            'Meta': {'object_name': 'Municipality'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.province': {
            'Meta': {'object_name': 'Province'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.status': {
            'Meta': {'object_name': 'Status'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_area.watermanagementarea': {
            'Meta': {'object_name': 'WaterManagementArea'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_esf.areaconfiguration': {
            'Meta': {'object_name': 'AreaConfiguration'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'esf_areaconfiguration_set'", 'to': "orm['lizard_area.Area']"}),
            'configuration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'esf_areaconfiguration_set'", 'to': "orm['lizard_esf.Configuration']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_comment': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '256', 'blank': 'True'}),
            'last_edit_by': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '256', 'blank': 'True'}),
            'last_edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'manual': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'manual_value': ('django.db.models.fields.DecimalField', [], {'default': '-999', 'max_digits': '15', 'decimal_places': '1'})
        },
        'lizard_esf.configuration': {
            'Meta': {'object_name': 'Configuration'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'configuration_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_esf.ConfigurationType']"}),
            'default_parameter_code_automatic_fews': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'default_parameter_code_final_fews': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'default_parameter_code_manual_fews': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'expanded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'source_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'value_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_esf.ValueType']"})
        },
        'lizard_esf.configurationtype': {
            'Meta': {'ordering': "['id']", 'object_name': 'ConfigurationType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
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
            'ident': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        'lizard_geo.geoobjectgroup': {
            'Meta': {'object_name': 'GeoObjectGroup'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'source_log': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['lizard_esf']
