from __future__ import absolute_import, unicode_literals

from soulcraft.celery import app
from soulcraft.msg.helpers import create_single_email


@app.task(name="send_email")
def send_email_task(to_email, body, attachment_buffer=None, attachment_filename=None):
    try:
        create_single_email(
            to_email, body, attachment_buffer=None, attachment_filename=None
        )
        return "Email Sent Successfully"
    except Exception as e:
        return str(e)
