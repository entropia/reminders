#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import datetime
import email.mime.text
import smtplib


SERVER = "localhost"
FROM = "bot@entropia.de"
TO = "intern@lists.entropia.de"
SUBJECT = "Erinnerung: morgen Hacker:innen-Frystyck"
MESSAGE_TMPL = """\
Liebe Entropianer,

Wie an jedem dritten Samstag im Monat ist morgen wieder geselliges
Hacker:innen-Frystyck [0].

Das bedeutet, dass ihr morgen um 11:23 Uhr mit $dingen zum Frühstücken
im Club sein solltet. Wenn ihr nicht wisst, was noch gebraucht wird,
schaut mal in die Einkaufsliste [1] oder entscheidet mit anderen
spontan vor Ort, was eingekauft werden muss.

Sollten die Räume nicht zugänglich, sein  findet das Frystyck 
im Cyber-Raum [2] statt.

Sollte etwas anderes angekündigt sein hat das
natürlich Vorrang vor dieser Erinnerung.

Viele Grüße
Ein Python-Script

[0] <https://entropia.de/Hackerfryhstyck>
[1] <https://entropia.pads.ccc.de/hackerfrystyck>
[2] <https://meet.entropia.de/hackerfryhstyck>

-- 
Dieses Schreiben wurde nicht mit systemd.maild versandt.
"""

def is_third_saturday(d):
    return d.isoweekday() == 6 and 15 <= d.day <= 21

def main():
    date = get_tomorrow()
    if is_third_saturday(date):
        message = build_message(date)
        send_reminder(message)

def get_tomorrow():
    now = datetime.datetime.today()
    today = now.date()
    tomorrow = now.date() + datetime.timedelta(days=1)
    return tomorrow

def build_message(time):
    msg = email.mime.text.MIMEText(MESSAGE_TMPL, "plain", "utf-8")
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    return msg

def send_reminder(msg):
    s = smtplib.SMTP(SERVER)
    s.sendmail(FROM, [TO], msg.as_string())
    s.quit()

if __name__ == "__main__":
    main()

