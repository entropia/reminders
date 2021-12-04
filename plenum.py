#!/usr/bin/env python3

"""
Plenum-Reminder, by Kunsi

To be executed by a cronjob every day at 00:01
Checks wether a Plenum is scheduled for the next day, if yes, it
sends out a mail notification to the intern mailing list.
"""

from datetime import date, timedelta
from locale import setlocale, LC_ALL
from os import environ
from sys import argv, exit

from email.mime.text import MIMEText
from requests import get
from smtplib import SMTP

URL = argv[1]

DEBUG = environ.get("DEBUG", "0") == "1"
DAYS = int(environ.get("DELTA_DAYS", 1))

tomorrow = date.today() + timedelta(days=DAYS)


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return


setlocale(LC_ALL, "de_DE.UTF-8")
wiki = get(URL).content.decode("utf-8")

plenum_tops = None
for date_format in ("%Y-%m-%d", "%d.%m.%Y"):
    start = "{} ===".format(tomorrow.strftime(date_format))
    plenum_tops = find_between(wiki, start, "=== ")

    if plenum_tops:
        break
else:
    # Catch a corner case for the first plenum on a page
    plenum_tops = find_between(wiki, start, "</textarea>")

if plenum_tops:
    template = """Hallo,
morgen ist (laut Wiki) wieder mal Plenum. Nachfolgend die Tagesordnungs-
punkte aus dem Wiki:

{}""".format(
        plenum_tops.strip()
    )

    if DEBUG:
        print(template)
        exit(0)

    msg = MIMEText(template)
    msg["Subject"] = "Plenum am %s" % tomorrow.strftime("%A, %d.%m.%Y")
    msg["From"] = argv[2]
    msg["To"] = argv[3]

    smtpObj = SMTP("localhost")
    smtpObj.send_message(msg)
    smtpObj.quit()
elif DEBUG:
    print(wiki)
    exit(1)
