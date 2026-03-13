from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    # Stripe
    STRIPE_API_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_SUCCESS_URL: str
    STRIPE_CANCEL_URL: str

    DEBUG: bool = True
    SECRET_KEY: str

    # Pydantic v2 config
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow" 
    }

settings = Settings()