import os
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()


def init_sentry():
    dsn = os.getenv("SENTRY_DSN")
    if not dsn:
        return
    sentry_sdk.init(
        dsn=dsn,
        traces_sample_rate=0,
        environment=os.getenv("ENV", "development"),
    )

def log_info(message):
    """Envoie un message d'information a Sentry."""
    sentry_sdk.capture_message(message, level="info")


def log_error(exception):
    """Envoie une exception a Sentry."""
    sentry_sdk.capture_exception(exception)