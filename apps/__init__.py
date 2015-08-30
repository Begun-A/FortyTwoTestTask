import datetime


FAKE_PATH_LIST = [
    '/fefw',
    '/12747630-426-13!@$*&_*&%!_)&@*$&__!#  *$!@$*_!%)(&#*$&&$)!(#$)(',
    '/',
    '/el/',
    '/www',
    '/1242',
    '/?d=3',
    '/?_=23423523',
    '/avaba-kedabra/',
    '/****/'
]
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
