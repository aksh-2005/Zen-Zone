"""
WSGI config for zenzone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "zenzone.settings"
)

application = get_wsgi_application()

# Serve media files via Whitenoise in production (Vercel)
media_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')
if os.path.isdir(media_path):
    application = WhiteNoise(application, root=media_path, prefix='media/')

app = application
