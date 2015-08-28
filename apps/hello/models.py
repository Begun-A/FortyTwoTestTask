from django.db import models
from PIL import Image


class Contact(models.Model):
    class Meta:
        db_table = 'Contact'

    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    birth_date = models.DateField()
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=25)
    other = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='images', blank=True, null=True)

    def save(self, size=(200, 200)):
        super(Contact, self).save()

        try:
            filename = str(self.photo.path)
            image = Image.open(filename)

            image.resize(size, Image.ANTIALIAS)
            image.save(filename)
        except (IOError, ValueError, AttributeError):
            pass
        return None


class LogWebRequest(models.Model):
    class Meta:
        db_table = 'LogWebRequest'

    method = models.CharField(max_length=16)
    path = models.CharField(max_length=1000)
    status_code = models.IntegerField()
    remote_addr = models.IPAddressField()
    time = models.DateTimeField(auto_now=True)


class SignalLog(models.Model):
    class Meta:
        db_table = 'SignalLog'

    action = models.CharField(max_length=16)
    model = models.CharField(max_length=25)
    time = models.DateTimeField(auto_now=True)
