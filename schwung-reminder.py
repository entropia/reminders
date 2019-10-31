#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Recommended usage: use cron:

0 19 * * * /path/to/script/...py >> /path/to/log.log 2&>1

Don't run this more than once per day.
19:00 seems like a good time.
"""

import datetime
import email.mime.text
import smtplib


__version__ = "1.0.5"

# Isoweekdays
FRIDAY = 5

# Configuration
SERVER = "localhost"
FROM = "bot@entropia.de"
TO = "intern@lists.entropia.de"
SUBJECT = "Erinnerung: morgen Schwung-Treffen"
MESSAGE_TMPL = """\
Liebe Entropianer,

wie an jedem ersten, zweiten und vierten Freitag im
Monat ist morgen ab %(begin)s ein Treffen der Schwung.

Und wie an jedem ersten Freitag im Monat findet dieses
Treffen morgen im Club statt.

Das bedeutet, dass ihr morgen lieber erst
etwas später in den Club kommen solltet.

Sollte unaufgeräumt sein: *heute* aufräumen!

Sollte etwas anderes angekündigt sein hat das
natürlich Vorrang vor dieser Erinnerung.

Viele Grüße
Ein Python-Script

--
Dieses Schreiben wurde maschinell erstellt
und ist auch ohne Unterschrift gültig.
"""
DAYS = {
    (FRIDAY, 1): "19:00",
}


def main():
    date = get_tomorrow()
    day = date.isoweekday(), get_weekday_in_month(date)
    print("%s: tomorrow is %i. %s in month => %s" % (
        datetime.datetime.today().strftime("%F %R"),
        day[1],
        date.strftime("%A"),
        "sending mail" if day in DAYS else "not sending mail")
        )
    if day in DAYS:
        start_time = DAYS[day]
        message = build_message(start_time)
        send_reminder(message)


def get_weekday_in_month(dt):
    num = 0
    for day_in_month in xrange(1, dt.day + 1):
        day_obj = datetime.date(dt.year, dt.month, day_in_month)
        if day_obj.isoweekday() == dt.isoweekday():
            num += 1
    return num


def get_tomorrow():
    now = datetime.datetime.today()
    today = now.date()
    tomorrow = today + datetime.timedelta(days=1)
    return tomorrow


def build_message(time):
    msg = email.mime.text.MIMEText(MESSAGE_TMPL % {"begin": time}, "plain", "utf-8")
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    return msg


def send_reminder(msg):
    s = smtplib.SMTP(SERVER)
    s.sendmail(FROM, [TO], msg.as_string())
    s.quit()


def test_get_weekday_in_month():
    assert 1 == get_weekday_in_month(datetime.date(2012, 8, 1))
    assert 1 == get_weekday_in_month(datetime.date(2012, 8, 3))
    assert 2 == get_weekday_in_month(datetime.date(2012, 8, 10))
    assert 3 == get_weekday_in_month(datetime.date(2012, 8, 17))
    assert 4 == get_weekday_in_month(datetime.date(2012, 8, 24))
    assert 5 == get_weekday_in_month(datetime.date(2012, 8, 31))
    assert 5 == get_weekday_in_month(datetime.date(2012, 4, 29))


if __name__ == "__main__":
    main()
