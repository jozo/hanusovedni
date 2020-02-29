# hanusovedni
# TODO add how to start develop

s = Site.objects.get()
s.hostname = "hanusovedni.online"
s.save()

from django.core.cache import cache
cache.clear()
