"""
WSGI config for making_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from django.core.wsgi import get_wsgi_application

project_folder =  Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'making_project.settings')

application = get_wsgi_application()
