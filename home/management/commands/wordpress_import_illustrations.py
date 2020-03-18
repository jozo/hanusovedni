from glob import glob

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.images.models import Image
from wagtail.search import index as search_index


class Command(BaseCommand):
    help = "Imports illustrations from Wordpress version of BHD"

    def add_arguments(self, parser):
        parser.add_argument(
            "--from-dir", "-f", type=str, help="Path to directory with images"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Importing images"))

        if not options["from_dir"].endswith("/"):
            options["from_dir"] = options["from_dir"] + "/"

        for filepath in sorted(glob(options["from_dir"] + "*-90x90.png")):
            with open(filepath, "rb") as image_file:
                name = filepath.split("/")[-1][:-10]
                image = Image(title=name)
                image.file = ImageFile(file=image_file, name=name+".png")
                image.file_size = image.file.size

                image.file.seek(0)
                image._set_file_hash(image.file.read())
                image.file.seek(0)

                # Reindex the image to make sure all tags are indexed
                search_index.insert_or_update_object(image)
                image.save()
                image.tags.add("illustration")

                self.stdout.write(self.style.SUCCESS(f"{image.pk},{image.title}"))

        self.stdout.write(self.style.SUCCESS("Importing images finished"))
