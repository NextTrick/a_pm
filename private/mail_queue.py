# -*- coding: utf-8 -*-
#__author__ = 'alfonsodg'
import time

while True:
    rows = db(db.mail_queue.status==1).select()
    for row in rows:
        email = row.email
        subject = row.subject
        message = row.content_message
        if email is None:
            continue
        if subject is None:
            continue
        if mail.send(to=email,
            subject=subject,
            message=message):
            row.update_record(status=2)
        else:
            row.update_record(status=0)
        db.commit()
    time.sleep(60) # check every minute