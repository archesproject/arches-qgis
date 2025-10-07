import os
from django.core.exceptions import ImproperlyConfigured

try:
    from .arches_qgis_project.settings import *
except ImportError:
    pass

def get_env_variable(var_name):
    msg = "Set the %s environment variable"
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = msg % var_name
        raise ImproperlyConfigured(error_msg)


ELASTICSEARCH_HOSTS = [
    {
        "scheme": "http",
        "host": get_env_variable("ESHOST"),
        "port": int(get_env_variable("ESPORT_CONTAINER")),
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": get_env_variable("ARCHES_PROJECT"),
        "USER": get_env_variable("PGUSERNAME"),
        "PASSWORD": get_env_variable("PGPASSWORD"),
        "HOST": get_env_variable("PGHOST"),
        "PORT": get_env_variable("PGPORT_CONTAINER"),
        "POSTGIS_TEMPLATE": "template_postgis",
    }
}

ARCHES_NAMESPACE_FOR_DATA_EXPORT = f"http://localhost:{get_env_variable("DJANGO_PORT")}"
PUBLIC_SERVER_ADDRESS = f"http://localhost:{get_env_variable("DJANGO_PORT")}"

OAUTH_CLIENT_ID = "ZmRsVUmUtwas8lmgX40PmgAQacESxxv9EPQdIm8S"

# Include name of docker container in allowed hosts
ALLOWED_HOSTS = ["localhost", "arches-qgis-arches"]