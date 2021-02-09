import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manga_viewer_api.settings')
django.setup()

