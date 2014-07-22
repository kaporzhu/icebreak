# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Order'
        db.create_table(u'orders_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shops.Shop'])),
            ('delivery_man', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Staff'], null=True, blank=True)),
            ('total_price', self.gf('django.db.models.fields.FloatField')()),
            ('coupon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coupons.Coupon'], null=True, blank=True)),
            ('discount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('delivery_time', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('time_frame', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['foods.TimeFrame'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='unpaid', max_length=32, db_index=True)),
            ('paid_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('steps', self.gf('django.db.models.fields.TextField')(default='{"on the way": {"date": "", "time": "", "is_done": false, "label": "\\u914d\\u9001\\u5458\\u51fa\\u53d1"}, "paid": {"date": "", "time": "", "is_done": false, "label": "\\u4ed8\\u6b3e"}, "packing done": {"date": "", "time": "", "is_done": false, "label": "\\u6253\\u5305\\u5b8c\\u6210"}, "distributing": {"date": "", "time": "", "is_done": false, "label": "\\u5230\\u8fbe\\u5199\\u5b57\\u697c"}, "unpaid": {"date": "", "time": "", "is_done": true, "label": "\\u4e0b\\u5355"}, "done": {"date": "", "time": "", "is_done": false, "label": "\\u5b8c\\u6210"}, "printed": {"date": "", "time": "", "is_done": false, "label": "\\u6253\\u5370\\u8ba2\\u5355"}}')),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['buildings.Building'])),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['buildings.Zone'], null=True, blank=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['buildings.Room'])),
        ))
        db.send_create_signal(u'orders', ['Order'])

        # Adding model 'OrderFood'
        db.create_table(u'orders_orderfood', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('food', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['foods.Food'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Order'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('count', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'orders', ['OrderFood'])


    def backwards(self, orm):
        # Deleting model 'Order'
        db.delete_table(u'orders_order')

        # Deleting model 'OrderFood'
        db.delete_table(u'orders_orderfood')


    models = {
        u'accounts.staff': {
            'Meta': {'object_name': 'Staff'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'delivery man'", 'max_length': '16'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shops.Shop']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'buildings.building': {
            'Meta': {'object_name': 'Building'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'floors': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_multiple': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shops.Shop']"})
        },
        u'buildings.room': {
            'Meta': {'object_name': 'Room'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['buildings.Building']"}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'floor': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['buildings.Zone']", 'null': 'True', 'blank': 'True'})
        },
        u'buildings.zone': {
            'Meta': {'object_name': 'Zone'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['buildings.Building']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'floors': ('django.db.models.fields.SmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'coupons.coupon': {
            'Meta': {'object_name': 'Coupon'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shop_coupons'", 'to': u"orm['auth.User']"}),
            'discount': ('django.db.models.fields.FloatField', [], {}),
            'expired_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shops.Shop']"}),
            'used_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'used_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'foods.food': {
            'Meta': {'object_name': 'Food'},
            'count': ('django.db.models.fields.SmallIntegerField', [], {'default': 'True'}),
            'count_today': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'sales': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shops.Shop']"}),
            'tips': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'foods.timeframe': {
            'Meta': {'object_name': 'TimeFrame'},
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'foods': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['foods.Food']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'sections': ('django.db.models.fields.TextField', [], {}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shops.Shop']"}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        u'orders.order': {
            'Meta': {'object_name': 'Order'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['buildings.Building']"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'coupon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coupons.Coupon']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'delivery_man': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Staff']", 'null': 'True', 'blank': 'True'}),
            'delivery_time': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'discount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'paid_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['buildings.Room']"}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shops.Shop']"}),
            'short_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'unpaid'", 'max_length': '32', 'db_index': 'True'}),
            'steps': ('django.db.models.fields.TextField', [], {'default': '\'{"on the way": {"date": "", "time": "", "is_done": false, "label": "\\\\u914d\\\\u9001\\\\u5458\\\\u51fa\\\\u53d1"}, "paid": {"date": "", "time": "", "is_done": false, "label": "\\\\u4ed8\\\\u6b3e"}, "packing done": {"date": "", "time": "", "is_done": false, "label": "\\\\u6253\\\\u5305\\\\u5b8c\\\\u6210"}, "distributing": {"date": "", "time": "", "is_done": false, "label": "\\\\u5230\\\\u8fbe\\\\u5199\\\\u5b57\\\\u697c"}, "unpaid": {"date": "", "time": "", "is_done": true, "label": "\\\\u4e0b\\\\u5355"}, "done": {"date": "", "time": "", "is_done": false, "label": "\\\\u5b8c\\\\u6210"}, "printed": {"date": "", "time": "", "is_done": false, "label": "\\\\u6253\\\\u5370\\\\u8ba2\\\\u5355"}}\''}),
            'time_frame': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['foods.TimeFrame']"}),
            'total_price': ('django.db.models.fields.FloatField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['buildings.Zone']", 'null': 'True', 'blank': 'True'})
        },
        u'orders.orderfood': {
            'Meta': {'object_name': 'OrderFood'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'count': ('django.db.models.fields.SmallIntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'food': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['foods.Food']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Order']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'shops.shop': {
            'Meta': {'object_name': 'Shop'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'close_tip': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'open_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['orders']