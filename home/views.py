from django.shortcuts import get_object_or_404, redirect

from home.models import Speaker, Event


def redirect_speakers(request, slug):
    speaker = get_object_or_404(Speaker, wordpress_url=slug)
    return redirect(speaker.get_url(), permanent=True)


def redirect_events(request, slug):
    event = get_object_or_404(Event, wordpress_url=slug)
    return redirect(event.get_url(), permanent=True)
