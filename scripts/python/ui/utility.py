import sys
import os

path = os.path.join(os.path.dirname(__file__), "../site-packages")
sys.path.insert(0, path)

from sentry_sdk import capture_exception
import sentry_sdk


sentry_sdk.init(
    dsn="https://907fc1d47a6b6e29691284fceac1d73c@o4507125362458624.ingest.us.sentry.io/4507125364162560",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

def get_human_readable(size):
    suffixes = ["bytes", "KB", "MB", "GB", "TB", "PB"]
    idx = 0
    while size >= 1024:
        size /= 1024
        idx += 1
    if idx == 0:
        return "{:.0f} {}".format(size, suffixes[idx])
    return "{:.2f} {}".format(size, suffixes[idx])


def capture_to_sentry(func):
    def wrapper():
        try:
            func()
        except Exception as e:
            # Alternatively the argument can be omitted
            capture_exception(e)
            raise e
    return wrapper
