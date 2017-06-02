import sys, os
sys.path.append('/path/to/your/django/app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
from scrape_poly_t import update_tt
import django.core as core
update_tt()