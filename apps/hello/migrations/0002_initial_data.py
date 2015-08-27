# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.contrib.auth.models import User


class Migration(DataMigration):

    def forwards(self, orm):
        orm.Contact.objects.create(
            bio="self.educated man, try to find himself in web development.",
            first_name="Bogdan",
            last_name="Kurinnyi",
            photo=None,
            other="Some other contacts",
            skype="DeV1doR",
            birth_date="1994-07-26",
            jabber="dev1dor@jabber.ua",
            email="dev1dor@ukr.net"
        )
        orm.User = User
        orm.User.objects.create_superuser(
            username="admin@admin.com",
            password="admin",
            email="admin@admin.com"
        )

    def backwards(self, orm):
        orm.Contact.objects.get(pk=1).delete()
        orm.User = User
        orm.User.objects.get(pk=1).delete()

    models = {
        u'hello.contact': {
            'Meta': {'object_name': 'Contact', 'db_table': "'Contact'"},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'other': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'hello.logwebrequest': {
            'Meta': {'object_name': 'LogWebRequest', 'db_table': "'LogWebRequest'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'remote_addr': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'status_code': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['hello']
    symmetrical = True
