from django.core.management.base import BaseCommand
from livres.models import Livre


class Command(BaseCommand):
    help = 'Update all Livre instances with "livre" in the titre to be indisponible'

    def handle(self, *args, **kwargs):
        livres_to_update = Livre.objects.filter(titre__icontains="livre")
        count = livres_to_update.update(disponible=False)
        self.stdout.write(self.style.SUCCESS(f'{count} livres updated to indisponible.'))
