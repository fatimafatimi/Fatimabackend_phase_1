import secrets  # <-- replaces random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.otp_model import OTP
from rate_limiter import RateLimiter
from utils.async_utils import run_async  # <-- import the wrapper

try:
    from redis_manager import RedisManager
    REDIS_ENABLED = True
except ImportError:
    REDIS_ENABLED = False

OTP_EXPIRY_MINUTES = 5
OTP_CACHE_TTL = OTP_EXPIRY_MINUTES * 60


def generate_otp():
    # secrets is cryptographically secure, random.randint is NOT
    return str(secrets.randbelow(900000) + 100000)


def create_otp(db: Session, user_id: int, purpose: str):
    allowed, remaining = RateLimiter.check_limit(
        key=f"otp_limit:{user_id}",
        max_requests=3,
        window_seconds=3600
    )

    if not allowed:
        raise ValueError("Too many OTP requests. Try again after 1 hour.")

    otp_code = generate_otp()
    expiry_time = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)

    otp = OTP(
        user_id=user_id,
        otp_code=otp_code,
        purpose=purpose,
        expiry_time=expiry_time
    )
    db.add(otp)
    db.commit()
    db.refresh(otp)

    if REDIS_ENABLED:
        redis_key = f"otp:{purpose}:{user_id}"
        try:
            run_async(RedisManager.set_key(redis_key, otp_code, ttl=OTP_CACHE_TTL))
        except Exception:
            pass  # Redis failure is non-fatal

    return otp


def verify_otp(db: Session, user_id: int, otp_code: str, purpose: str):
    if REDIS_ENABLED:
        redis_key = f"otp:{purpose}:{user_id}"
        try:
            cached = run_async(RedisManager.get_key(redis_key))
            if cached is not None and cached != otp_code:
                return False, "Invalid OTP"
        except Exception:
            pass  # Redis failure → fall through to DB

    otp = (
        db.query(OTP)
        .filter(
            OTP.user_id == user_id,
            OTP.otp_code == otp_code,
            OTP.purpose == purpose,
            OTP.is_used == False
        )
        .first()
    )

    if not otp:
        return False, "Invalid OTP"

    if otp.expiry_time < datetime.utcnow():
        return False, "OTP expired"

    otp.is_used = True
    otp.is_verified = True
    db.commit()

    if REDIS_ENABLED:
        try:
            run_async(RedisManager.delete_key(f"otp:{purpose}:{user_id}"))
        except Exception:
            pass

    return True, "OTP verified"


# these two functions don't touch Redis so no changes needed
def check_otp_verified(db: Session, user_id: int, purpose: str) -> bool:
    otp = (
        db.query(OTP)
        .filter(
            OTP.user_id == user_id,
            OTP.purpose == purpose,
            OTP.is_used == True,
            OTP.is_verified == True
        )
        .order_by(OTP.created_at.desc())
        .first()
    )
    return otp is not None


def consume_verified_otp(db: Session, user_id: int, purpose: str):
    otp = (
        db.query(OTP)
        .filter(
            OTP.user_id == user_id,
            OTP.purpose == purpose,
            OTP.is_used == True,
            OTP.is_verified == True
        )
        .order_by(OTP.created_at.desc())
        .first()
    )
    if otp:
        otp.is_verified = False
        db.commit()