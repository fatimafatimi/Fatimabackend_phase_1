# utils/otp_utils.py
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.otp_model import OTP

OTP_EXPIRY_MINUTES = 5

def generate_otp():
    return str(random.randint(100000, 999999))

def create_otp(db: Session, user_id: int, purpose: str):
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
    return otp


def verify_otp(db: Session, user_id: int, otp_code: str, purpose: str):
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
    otp.is_verified = True  # mark as verified — unlocks reset-password
    db.commit()

    return True, "OTP verified"


def check_otp_verified(db: Session, user_id: int, purpose: str) -> bool:
    # checks if user has a recently verified OTP that hasn't been consumed yet
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
    # called after password reset — clears the verified flag so it can't be reused
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