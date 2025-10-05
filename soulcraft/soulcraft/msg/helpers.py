
from django.conf import settings
from django.utils.html import escape
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, Mail
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


def create_single_email(data):
    """
    Send a contact email using a dict from ContactForm.cleaned_data.
    Expected keys: name, email, subject, message, topic.
    Includes try/except to catch and log SendGrid issues.
    """
    try:
        # --- Extract and sanitize form data ---
        name = data.get("name", "").strip()
        from_email = data.get("email", "").strip()
        subject_input = data.get("subject", "Website inquiry").strip()
        topic = data.get("topic", "general").lower()
        message = data.get("message", "")

        topic_labels = {
            "services": "Carwash Services",
            "platform": "Platform / Demo",
            "general": "General",
        }
        topic_label = topic_labels.get(topic, "General")
        subject = f"[{topic_label}] {subject_input}"

        # --- Escape & format message content ---
        safe_message = escape(message).replace("\n", "<br>")
        safe_name = escape(name)
        safe_from_email = escape(from_email)
        safe_topic = escape(topic_label)
        safe_subject = escape(subject_input)

        html_body = (
            f"<p><strong>New website inquiry</strong></p>"
            f"<p>"
            f"<strong>Name:</strong> {safe_name}<br>"
            f"<strong>Email:</strong> {safe_from_email}<br>"
            f"<strong>Topic:</strong> {safe_topic}<br>"
            f"<strong>Subject:</strong> {safe_subject}"
            f"</p>"
            f"<p><strong>Message:</strong><br>{safe_message}</p>"
        )

        # --- Recipient setup ---
        to_email = getattr(settings, "CONTACT_TO_EMAIL", None)
        if not to_email:
            raise ValueError("CONTACT_TO_EMAIL is not defined in settings.py")

        # --- Build SendGrid Mail object ---
        mail = Mail(
            from_email=settings.MAIL_DEFAULT_SENDER,
            to_emails=to_email,
            subject=subject,
            html_content=html_body,
        )

        if from_email:
            mail.reply_to = Email(from_email, name or None)

        # --- Send via SendGrid ---
        print("📧 Sending email to:", to_email)
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(mail)

        print("📬 SendGrid response code:", response.status_code)
        print("📬 SendGrid response body:", response.body)
        print("📬 SendGrid response headers:", response.headers)

        if response.status_code != 202:
            raise Exception(f"SendGrid failed with status {response.status_code}")

        return True

    except Exception as e:
        print("❌ Error sending email:", e)
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
