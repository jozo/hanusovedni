import os

import requests
from django.dispatch import receiver
from wagtail.contrib.frontend_cache.utils import PurgeBatch
from wagtail.core.signals import page_published, page_unpublished

from home.models.data_models import Event, Speaker
from home.models.pages import (
    EventIndexPage,
    FestivalPage,
    HomePage,
    ProgramIndexPage,
    logger,
)


class CloudFlare:
    def __init__(self, environments=None, zone_id=None, token=None) -> None:
        self.environments = environments or ["staging", "production"]
        self.zone_id = zone_id or os.environ["CLOUDFLARE_ZONEID"]
        self.token = token or os.environ["CLOUDFLARE_BEARER_TOKEN"]

    def purge_everything(self):
        if os.environ["ENVIRONMENT"] in self.environments:
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
        return pages


@receiver([page_published, page_unpublished], sender=Event)
@receiver([page_published, page_unpublished], sender=Speaker)
@receiver([page_published, page_unpublished], sender=FestivalPage)
def purge_cache_for_index_pages(**kwargs):
    batch = PurgeBatch()
    batch.add_pages(IndexPages().set())
    batch.purge()
