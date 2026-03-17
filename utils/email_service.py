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

def send_email(to_email: str, subject: str, body: str):
    try:
        message = MIMEMultipart()
        message["From"] = EMAIL_FROM
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, to_email, message.as_string())

        print(f"Email sent successfully to {to_email}")

    except Exception as e:
        print(f"Error sending email: {str(e)}")


def send_payment_success_email(user_email: str, plan_name: str, amount: str):
    template = env.get_template("payment_success.html")
    body = template.render(plan_name=plan_name, amount=amount)

    subject = "Payment Successful - Mini PMS"
    send_email(user_email, subject, body)
    
    
def send_payment_failed_email(user_email: str):
    template = env.get_template("payment_failed.html")
    body = template.render()
    send_email(user_email, "Payment Failed - Mini PMS", body)

def send_subscription_cancelled_email(user_email: str):
    template = env.get_template("subscription_cancelled.html")
    body = template.render()
    send_email(user_email, "Subscription Cancelled - Mini PMS", body)