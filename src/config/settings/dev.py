from config.settings.base import *  # noqa:

DEBUG = True

CURRENT_ENV = "DEV"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    "/usr/local/lib/python3.9/dist-packages/django/contrib/admin/static/admin",
)

STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        },
    }
elif os.environ.get("TEST_DB"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "oldtimers",
            "USER": "admin",
            "PASSWORD": "admin",
            "HOST": "localhost",
            "PORT": "5433",
        }
    }

    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.postgresql",
    #         "NAME": os.environ["POSTGRES_DB"],
    #         "USER": os.environ["POSTGRES_USER"],
    #         "PASSWORD": os.environ["POSTGRES_PASSWORD"],
    #         "HOST": os.environ["POSTGRES_HOST"],
    #         "PORT": os.environ["POSTGRES_PORT"],
    #     }
    # }

    #     "default": {
    #             "ENGINE": "django.db.backends.postgresql",
    #             "NAME": "oldtimers",
    #             "USER": "admin",
    #             "PASSWORD": "admin",
    #             "HOST": "localhost",
    #             "PORT": "5433",
    #     }
    # }
