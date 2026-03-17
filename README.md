# Email Notification System

## Overview

The Email Notification System is designed to send automated emails to users based on key events within the application, such as successful payments, failed transactions, and subscription cancellations. It ensures that users are consistently informed about their account and billing activities.

---

## Features

* Sends email notifications for successful payments
* Sends email notifications for failed transactions
* Sends email notifications when a subscription is cancelled
* Uses asynchronous processing to avoid blocking API responses
* Supports dynamic HTML email templates

---

## Tech Stack

* FastAPI (backend framework)
* SMTP (Gmail) for email delivery
* Jinja2 for HTML template rendering
* smtplib for sending emails
* python-dotenv for environment variable management

---

## Project Structure

```id="wf8ls5"
project/
│
├── config/
│   └── email_config.py
│
├── utils/
│   └── email_service.py
│
├── templates/
│   └── emails/
│       ├── payment_success.html
│       ├── payment_failed.html
│       └── subscription_cancelled.html
│
├── routers/
│   ├── webhook_router.py
│   └── subscription_router.py
```

---

## Environment Variables

Create a `.env` file in the root directory and configure the following:

```id="9trhk6"
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=Mini PMS <your_email@gmail.com>
```

---

## Steps to Run

### 1. Clone the Repository

```bash id="z3k91p"
git clone <your-repository-url>
cd <your-project-folder>
```

### 2. Create and Activate Virtual Environment

```bash id="u9a2bc"
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash id="p0m4tx"
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file and add your SMTP credentials (as shown above).

### 5. Run FastAPI Server

```bash id="b7s1qk"
uvicorn main:app --reload
```

### 6. Start Stripe Webhook Listener

```bash id="e4x8zn"
stripe listen --forward-to localhost:8000/webhooks/stripe
```

### 7. Test the System

* Perform a successful payment → success email should be sent
* Use Stripe test card for failure → failure email should be sent
* Cancel subscription → cancellation email should be sent

---

## Workflow

### Payment Success

When a user completes a payment, Stripe sends a `checkout.session.completed` event. The backend processes the subscription and sends a success email to the user.

### Payment Failure

If a payment fails, Stripe sends a `payment_intent.payment_failed` event. The system extracts the user’s email and sends a failure notification.

### Subscription Cancellation

When a user cancels an active subscription, the system updates the database and sends a cancellation confirmation email.

---

## Asynchronous Processing

Email notifications are sent using FastAPI BackgroundTasks. This ensures that email sending does not delay API responses or webhook handling.

---

## Notes

* Email delivery is non-blocking and does not affect core application logic
* The system relies on Stripe webhooks for accurate payment status updates

---
