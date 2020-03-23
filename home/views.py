from django.shortcuts import get_object_or_404, redirect
from django.views.defaults import page_not_found
from sentry_sdk import capture_message

from home.models import Speaker, Event


def redirect_speakers(request, slug):
    speaker = get_object_or_404(Speaker, wordpress_url=slug)
    return redirect(speaker.get_url(), permanent=True)


def redirect_events(request, slug):
    event = get_object_or_404(Event, wordpress_url=slug)
    return redirect(event.get_url(), permanent=True)


def handler404(request, exception):
    # capture_message(f"Error 404 {request.path}")
    return page_not_found(request, exception)
