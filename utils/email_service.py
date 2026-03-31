# utils/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from config.email_config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM

BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = BASE_DIR / "templates" / "emails"
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

TEST_EMAIL_DOMAINS = ["test.com", "fake.com", "example.com", "mailinator.com", "yopmail.com"]

def is_test_email(email: str) -> bool:
    domain = email.split("@")[-1].lower()
    return domain in TEST_EMAIL_DOMAINS


def send_email(to: str, subject: str, template_name: str, context: dict):
    if is_test_email(to):
        print(f"[TEST EMAIL] To: {to} | Subject: {subject} | Context: {context}")
        return

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
        # never crash the app because of email failure
        print(f"Error sending email to {to}: {str(e)}")



def send_payment_success_email(user_email: str, plan_name: str, amount: str, login_email: str, password: str):
    send_email(
        to=user_email,
        subject="Payment Successful - Mini PMS",
        template_name="payment_success.html",
        context={
            "plan_name": plan_name,
            "amount": amount,
            "login_email": login_email,
            "password": password
        }
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


def send_user_welcome_email(user_email: str, username: str):
    """Sent to normal user right after they are created — before payment."""
    send_email(
        to=user_email,
        subject="Account Request Received - Mini PMS",
        template_name="user_welcome.html",
        context={"username": username}
    )


def send_tenant_admin_welcome_email(admin_email: str, username: str, company_name: str):
    """Sent to tenant admin right after super admin creates their account."""
    send_email(
        to=admin_email,
        subject="Your Admin Account is Ready - Mini PMS",
        template_name="tenant_admin_welcome.html",
        context={"username": username, "company_name": company_name}
    )


def send_tenant_admin_payment_notification(admin_email: str, admin_username: str, user_email: str, username: str, plan_name: str):
    """Sent to tenant admin after one of their users completes payment."""
    send_email(
        to=admin_email,
        subject=f"User Payment Confirmed - {username} - Mini PMS",
        template_name="tenant_admin_payment_notification.html",
        context={
            "admin_username": admin_username,
            "username": username,
            "user_email": user_email,
            "plan_name": plan_name
        }
    )