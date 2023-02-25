import logging
import os

import requests
from django.conf import settings
from django.dispatch import receiver
from django.urls import reverse
from wagtail.contrib.frontend_cache.utils import PurgeBatch
from wagtail.signals import page_published, page_unpublished

from home.models.data_models import Event, Speaker
from home.models.pages import (
    EventIndexPage,
    FestivalPage,
    HomePage,
    ProgramIndexPage,
    SpeakerIndexPage,
    StreamPage,
)

logger = logging.getLogger(__name__)


class CloudFlare:
    def __init__(self, environments=None, zone_id=None, token=None) -> None:
        self.environments = environments or ["staging", "production"]
        self.zone_id = zone_id or os.environ.get("CLOUDFLARE_ZONEID")
        self.token = token or os.environ.get("CLOUDFLARE_BEARER_TOKEN")

    def purge_everything(self):
        if os.environ.get("ENVIRONMENT") in self.environments:
            url = (
                f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/purge_cache"
            )
            headers = {"Authorization": f"Bearer {self.token}"}
            logger.info(f"Purge everything in cache. {headers} {url}")

            response = requests.post(
                url, json={"purge_everything": True}, headers=headers
            )
            response.raise_for_status()


class IndexPages:
    def set(self):
        pages = set()
        pages.add(HomePage.objects.get())
        for event_index in EventIndexPage.objects.live():
            pages.add(event_index)
        for program_index in ProgramIndexPage.objects.live():
            pages.add(program_index)
        for festival_page in FestivalPage.objects.live():
            pages.add(festival_page)
        for speaker_index in SpeakerIndexPage.objects.live():
            pages.add(speaker_index)
        return pages


@receiver([page_published, page_unpublished], sender=Event)
@receiver([page_published, page_unpublished], sender=Speaker)
@receiver([page_published, page_unpublished], sender=FestivalPage)
def purge_cache_for_index_pages(**kwargs):
    batch = PurgeBatch()
    batch.add_pages(IndexPages().set())
    batch.add_url(settings.BASE_URL + "/en/events/json/")
    batch.add_url(settings.BASE_URL + "/sk/events/json/")
    batch.purge()


@receiver([page_published, page_unpublished], sender=StreamPage)
def purge_cache_for_api(**kwargs):
    batch = PurgeBatch()
    batch.add_url(settings.BASE_URL + reverse("api-stream"))
    batch.add_url(settings.BASE_URL + "/en/stream/")
    batch.add_url(settings.BASE_URL + "/sk/stream/")
    batch.purge()
