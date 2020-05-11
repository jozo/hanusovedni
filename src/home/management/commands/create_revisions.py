from django.core.management.base import BaseCommand
from django.db import transaction

from home.models import Event

MODEL_MAP = {"event": Event}


class Command(BaseCommand):
    help = "Create a revision for all pages of provided model"

    def add_arguments(self, parser):
        parser.add_argument(
            "--model-name",
            "-m",
            type=str,
            help=f"Model name, one of {MODEL_MAP.keys()}",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Started"))

        klass = MODEL_MAP[options["model_name"]]
        for i, instance in enumerate(klass.objects.iterator()):
            revision = instance.save_revision()
            revision.publish()

        self.stdout.write(self.style.SUCCESS(f"Finished - {i + 1} objects updated"))
