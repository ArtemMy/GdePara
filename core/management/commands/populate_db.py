from django.core.management.base import BaseCommand
from core.scrape_poly_t import update_tt

class Command(BaseCommand):
    def _populate(self):
    	update_tt()

    def handle(self, *args, **options):
        self._populate()