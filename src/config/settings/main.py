from config.settings.base import *  # noqa:

DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "ec2-3-127-255-223.eu-central-1.compute.amazonaws.com",
]

STATIC_ROOT = os.path.join(BASE_DIR, "static/oldtimers")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


CURRENT_ENV = "MAIN"
print(CURRENT_ENV)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    # "default_pg": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": os.environ["POSTGRES_DB"],
    #     "USER": os.environ["POSTGRES_USER"],
    #     "PASSWORD": os.environ["POSTGRES_PASSWORD"],
    #     "HOST": os.environ["POSTGRES_HOST"],
    #     "PORT": os.environ["POSTGRES_PORT"],
    # },
}
