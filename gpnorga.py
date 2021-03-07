#!/usr/bin/python3

#####
#
# Plenum-Reminder, by Kunsi
#
# To be executed by a cronjob every day at 00:01
#
# Checks wether a Plenum is scheduled for the next day, if yes, it
# sends out a mail notification to the intern mailing list.
#
#####

import requests
import datetime
import smtplib
import locale
from email.mime.text import MIMEText

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

def find_between( s, first, last ):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return None

today = datetime.date.today()
sunday = today + datetime.timedelta(days=1)

wiki = requests.get("https://entropia.de/index.php?title=GPN20:Orga/Tops&action=edit")
wikisource = wiki.content.decode('utf-8')

key_start = sunday.strftime('%d.%m.%Y') + ' ==='
key_end   = '=== '

plenum_tops = find_between(wikisource, key_start, key_end)

if plenum_tops:
    msg = MIMEText("""Hallo,
morgen ist (laut Wiki) wieder mal GPN-Orga-Treffen. Nachfolgend die
Tagesordnungspunkte aus dem Wiki:


""" + plenum_tops)

    msg['Subject'] = 'GPN-Orgatreffen am %s' % sunday.strftime('%A, %d.%m.%Y')
    msg['From'] = 'entropia@kaito.kunbox.net'
    msg['To'] = 'gpnorga@lists.entropia.de'

    smtpObj = smtplib.SMTP('localhost')
    smtpObj.send_message(msg)
    smtpObj.quit()

    print(msg)
