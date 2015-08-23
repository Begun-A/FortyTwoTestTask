from django.db import models


class Contact(models.Model):
    class Meta:
        db_table = 'Contact'

    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    birth_date = models.DateField()
    bio = models.TextField()
    contacts = models.CharField(max_length=16)
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=25)
    other = models.TextField(null=True)


class LogWebRequest(models.Model):
    class Meta:
        db_table = 'LogWebRequest'

    method = models.CharField(max_length=16)
    path = models.CharField(max_length=1000)
    status_code = models.IntegerField()
    remote_addr = models.IPAddressField()
    time = models.DateTimeField(auto_now=True)
