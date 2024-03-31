import base64

from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    ContentId,
    Disposition,
    FileContent,
    FileName,
    FileType,
    Mail,
)
from twilio.base.exceptions import TwilioException
from twilio.rest import Client

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
twilio_from = settings.TWILIO_FROM
twilio_verify_sid = settings.TWILIO_VERIFY_SID
notify_service_sid = settings.TWILIO_NOTIFY_SERVICE_SID

client = Client(account_sid, auth_token)

sg = SendGridAPIClient(settings.SENDGRID_API_KEY)

# whatsapp message


def create_single_email(
    to_email, body, attachment_buffer=None, attachment_filename=None
):
    subject = "received from website"
    message = Mail(
        from_email=settings.MAIL_DEFAULT_SENDER,
        to_emails=to_email,
        subject=subject,
        html_content=body,
    )
    if attachment_buffer and attachment_filename:
        # Create an attachment
        attachment = Attachment()
        attachment.file_content = FileContent(
            base64.b64encode(attachment_buffer.read()).decode()
        )
        attachment.file_name = FileName(attachment_filename)
        attachment.file_type = FileType("application/pdf")
        attachment.disposition = Disposition("attachment")
        attachment.content_id = ContentId("Attachment")

        # Add the attachment to the message
        message.attachment = attachment

    response = sg.send(message)
    # Handle the response and return an appropriate value based on your requirements
    if response.status_code == 202:
        return True
    else:
        print("Failed to send email. Error code:", response.status_code)
        return False


def send_sms(phone_number, body):
    try:
        message = client.messages.create(
            body=body,
            from_=twilio_from,
            to=phone_number,
        )
        return message.sid
    except Exception as e:
        print("Failed to send SMS:", str(e))
    return None


def _get_twilio_verify_client():
    return Client(account_sid, auth_token).verify.services(twilio_verify_sid)


def request_verification_token(phone):
    verify = _get_twilio_verify_client()
    try:
        verify.verifications.create(to=phone, channel="sms")
    except TwilioException:
        verify.verifications.create(to=phone, channel="call")


def check_verification_token(phone, token):
    verify = _get_twilio_verify_client()
    try:
        result = verify.verification_checks.create(to=phone, code=token)
    except TwilioException:
        return False
    return result.status == "approved"
