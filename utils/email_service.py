# utils/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from config.email_config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM

# Jinja2 environment
BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = BASE_DIR / "templates" / "emails"
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

def send_email(to: str, subject: str, template_name: str, context: dict):
    try:
        template = env.get_template(template_name)
        body = template.render(**context)

        message = MIMEMultipart()
        message["From"] = EMAIL_FROM
        message["To"] = to
        message["Subject"] = subject

        message.attach(MIMEText(body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, to, message.as_string())

        print(f"Email sent successfully to {to}")

    except Exception as e:
        print(f"Error sending email: {str(e)}")



def send_payment_success_email(user_email: str, plan_name: str, amount: str):
    send_email(
        to=user_email,
        subject="Payment Successful - Mini PMS",
        template_name="payment_success.html",
        context={"plan_name": plan_name, "amount": amount}
    )


def send_payment_failed_email(user_email: str):
    send_email(
        to=user_email,
        subject="Payment Failed - Mini PMS",
        template_name="payment_failed.html",
        context={}
    )


def send_subscription_cancelled_email(user_email: str):
    send_email(
        to=user_email,
        subject="Subscription Cancelled - Mini PMS",
        template_name="subscription_cancelled.html",
        context={}
    )