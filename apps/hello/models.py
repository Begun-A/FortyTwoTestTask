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

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def save(self, size=(200, 200)):

        super(Contact, self).save()

        try:
            pw = self.photo.width
            ph = self.photo.height
            nw = size[0]
            nh = size[1]

            # only do this if the image needs resizing
            if (pw, ph) != (nw, nh):
                filename = str(self.photo.path)
                image = Image.open(filename)
                pr = float(pw) / float(ph)
                nr = float(nw) / float(nh)

                if pr > nr:
                    # photo aspect is wider than destination ratio
                    th = int(round(nw / pr))
                    image = image.resize((nw, th), Image.ANTIALIAS)
                elif pr < nr:
                    # photo aspect is taller than destination ratio
                    tw = int(round(nh * pr))
                    image = image.resize((tw, nw), Image.ANTIALIAS)
                else:
                    # photo aspect matches the destination ratio
                    image = image.resize(size, Image.ANTIALIAS)

                image.save(filename)

        except ValueError:
            pass


class LogWebRequest(models.Model):
    class Meta:
        db_table = 'LogWebRequest'

    method = models.CharField(max_length=16)
    path = models.CharField(max_length=1000)
    status_code = models.IntegerField()
    remote_addr = models.IPAddressField()
    time = models.DateTimeField(auto_now=True)
    priority = models.IntegerField(default=0)

    def __unicode__(self):
        return u'Request: %s, priority: %s' % (
            self.pk,
            self.priority
        )


class SignalLog(models.Model):
    class Meta:
        db_table = 'SignalLog'

    action = models.CharField(max_length=16)
    model = models.CharField(max_length=25)
    time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s %s' % (self.model, self.action)
