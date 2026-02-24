import os

import tusk_drift_init  # noqa: F401

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
