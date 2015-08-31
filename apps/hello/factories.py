import datetime
"""
import factory
import factory.fuzzy
from models import (
    Contact,
    LogWebRequest,
    SignalLog
)
"""

FAKE_PATH_LIST = (
    '/fefw',
    '/12747630-426-13!@$*&_*&%!_)&@*$&__!#  *$!@$*_!%)(&#*$&&$)!(#$)(',
    '/',
    '/el/',
    '/www',
    '/1242',
    '/?d=3',
    '/?_=23423523',
    '/avaba-kedabra/',
    '/****/',
)
FAKE_DATA = {
    u"first_name": u"hello",
    u"last_name": u"world",
    u"skype": u"gogogo",
    u"birth_date": unicode(
        datetime.datetime.utcnow().strftime("%Y-%m-%d")
    ),
    u"jabber": u"jaber@jaber.com",
    u"email": u"email@email.com",
    u"bio": u"",
    u"other": u"",
    u"photo": u""
}

FAKE_METHODS = ('GET', 'POST', 'PUT', 'DELETE')
FAKE_STATUSES = (200, 302, 404, 500)
FAKE_ADDRS = ('127.0.0.1', '942.4.3.1', '234.5.1.6')


"""
class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    first_name = factory.Sequence(lambda n: 'first_name_%s' % n)
    last_name = factory.Sequence(lambda n: 'last_name_%s' % n)
    birth_date = factory.Sequence(
        lambda n: datetime.date(2000, 1, 1) + datetime.timedelta(days=n)
    )
    bio = factory.Sequence(lambda n: 'some_bio_%s' % n)
    email = factory.Sequence(lambda n: 'email_%s@email.com' % n)
    jabber = factory.Sequence(lambda n: 'jabber_%s@jabber.com' % n)
    skype = factory.Sequence(lambda n: 'skype_%s' % n)
    other = factory.Sequence(lambda n: 'some_other_%s' % n)
    photo = factory.Sequence(lambda n: 'photo_%s.jpg' % n)


class LogWebRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LogWebRequest

    method = factory.Iterator(FAKE_METHODS)
    path = factory.Iterator(FAKE_PATH_LIST)
    status_code = factory.Iterator(FAKE_STATUSES)
    remote_addr = factory.Iterator(FAKE_ADDRS)
    time = factory.Sequence(
        lambda n: datetime.date(2000, 1, 1) + datetime.timedelta(days=n)
    )
    priority = factory.fuzzy.FuzzyInteger(1)


class SignalLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SignalLog

    action = factory.Iterator(['added', 'updated', 'deleted'])
    model = factory.Iterator([
        Contact.__name__,
        LogWebRequest.__name__,
        SignalLog.__name__
    ])
    time = factory.Sequence(
        lambda n: datetime.date(2000, 1, 1) + datetime.timedelta(days=n)
    )
"""
