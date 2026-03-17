# Payment Module (FastAPI + Stripe)

A complete **Payment Module** implementation using **FastAPI** with **Stripe integration**.  
This module supports user subscriptions, payment processing, and secure token-based authorization.

---

## Features

- **User Authentication & Authorization**
  - Login and register users
  - JWT-based token authentication
  - Role-based access (Admin vs User)
  
- **Stripe Payment Integration**
  - One-time payments
  - Subscription payments
  - Webhook support for payment events
  - Sandbox (test) and live modes

- **Secure & Scalable**
  - Passwords hashed with industry-standard algorithms
  - Sensitive data secured via environment variables
  - Easily extendable for future payment gateways

---

## Tech Stack

- **Backend:** FastAPI, Python 3.11+
- **Database:** PostgreSQL / SQLite
- **ORM:** SQLAlchemy
- **Payment Gateway:** Stripe
- **Authentication:** JWT (JSON Web Tokens)
- **Dependencies:** `stripe`, `python-dotenv`, `pydantic`, `fastapi`, `uvicorn`

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/fatimafatimi/payment_module.git
cd payment-module
````

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./test.db      # or your PostgreSQL URL
STRIPE_API_KEY=sk_test_yourkey
STRIPE_WEBHOOK_SECRET=whsec_yoursecret
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Usage

### Run the server

```bash
uvicorn main:app --reload
```

7. Access Swagger UI at:

```
http://127.0.0.1:8000/docs
Your API will be available at `http://127.0.0.1:8000/docs`.

---

## Endpoints

### **Authentication**

| Method | Endpoint          | Description                     | Access    |
| ------ | ----------------- | ------------------------------- | --------- |
| POST   | `/users/login`    | Login user and get JWT token    | Public    |
| POST   | `/users/register` | Admin-only: create a new user   | Admin     |
| GET    | `/users/me`       | Get current logged-in user info | Protected |

---

### **Plan Management**

| Method | Endpoint      | Description             | Access             |
| ------ | ------------- | ----------------------- | ------------------ |
| GET    | `/plans/`     | Get all available plans | Public / Protected |
| GET    | `/plans/{id}` | Get plan details by ID  | Public / Protected |
| POST   | `/plans/`     | Create a new plan       | Admin              |
| PUT    | `/plans/{id}` | Update an existing plan | Admin              |
| DELETE | `/plans/{id}` | Delete a plan           | Admin              |

---

### **Subscription**

| Method | Endpoint               | Description                                              | Access    |
| ------ | ---------------------- | -------------------------------------------------------- | --------- |
| GET    | `/subscription/me`     | Get current user’s active or last subscription           | Protected |
| GET    | `/subscription/status` | Get status of current subscription                       | Protected |
| POST   | `/subscription/cancel` | Cancel active subscription (Stripe + DB)                 | Protected |
| POST   | `/subscription/create` | (Optional) Create a new subscription via Stripe Checkout | Protected |

---

### **Payments**

| Method | Endpoint                            | Description                                 | Access    |
| ------ | ----------------------------------- | ------------------------------------------- | --------- |
| POST   | `/payments/create-checkout-session` | Create a Stripe Checkout session for a plan | Protected |
| GET    | `/payments/my-payments`             | Get logged-in user's payment history        | Protected |
| GET    | `/payments/`                        | Get all payments (Admin view)               | Admin     |

---

### **Webhook**

| Method | Endpoint           | Description                                        | Access                |
| ------ | ------------------ | -------------------------------------------------- | --------------------- |
| POST   | `/webhooks/stripe` | Stripe webhook for subscription and payment events | Stripe only (no auth) |

---

### **Premium / Feature Access**

| Method | Endpoint           | Description                        | Access                      |
| ------ | ------------------ | ---------------------------------- | --------------------------- |
| GET    | `/premium/content` | Access premium content or features | Protected / Paid users only |


---

### Testing Stripe (Sandbox Mode)

1. Use **Stripe test API keys** from [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys)
2. Use **Stripe CLI** to test webhooks:

```bash
stripe listen --forward-to http://127.0.0.1:8000/webhook
```

3. Trigger test events:

```bash
stripe trigger payment_intent.succeeded
```

> All test payments can be made with Stripe test cards, e.g. `4242 4242 4242 4242`.

---

## Folder Structure

```
payment-module/
│
├─ main.py                 # FastAPI app entry
├─ database.py             # Database connection & session
├─ models/                 # SQLAlchemy models (User, Subscription)
├─ schemas/                # Pydantic schemas
├─ dependencies/           # JWT auth and dependencies
├─ handler/                # Business logic (login, payments)
├─ utils/                  # Stripe service & helpers
└─ tests/                  # Unit and integration tests
```

---

## Benefits of This RBAC System

* **Flexible access control** – Assign permissions at the role level.
* **Secure** – Users can only access actions allowed by their role.
* **Scalable** – Easily add new roles and permissions without changing code.
* **Traceable** – Easy to see which role has what permissions.

---

## Security

* JWT tokens are required for all protected endpoints
* Admin-only routes require elevated privileges
* Stripe webhook events are verified using the `STRIPE_WEBHOOK_SECRET`

---
