# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'CanadianTaxRate'
        db.create_table('canada_tax_canadiantaxrate', (
            ('override', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('taxCode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('compound_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('taxrate_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['area.TaxRate'], unique=True, primary_key=True)),
            ('compound', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('canada_tax', ['CanadianTaxRate'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'CanadianTaxRate'
        db.delete_table('canada_tax_canadiantaxrate')
    
    
    models = {
        'area.taxrate': {
            'Meta': {'object_name': 'TaxRate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '6'}),
            'taxClass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.TaxClass']"}),
            'taxCountry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['l10n.Country']", 'null': 'True', 'blank': 'True'}),
            'taxZone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['l10n.AdminArea']", 'null': 'True', 'blank': 'True'})
        },
        'canada_tax.canadiantaxrate': {
            'Meta': {'object_name': 'CanadianTaxRate', '_ormbases': ['area.TaxRate']},
            'compound': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'compound_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'override': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'taxCode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'taxrate_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['area.TaxRate']", 'unique': 'True', 'primary_key': 'True'})
        },
        'l10n.adminarea': {
            'Meta': {'object_name': 'AdminArea'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['l10n.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'l10n.country': {
            'Meta': {'object_name': 'Country'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'admin_area': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'numcode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'product.taxclass': {
            'Meta': {'object_name': 'TaxClass'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }
    
    complete_apps = ['canada_tax']
