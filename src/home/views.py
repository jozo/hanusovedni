from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import check_for_language
from django.views.defaults import page_not_found

from home.models import ArchiveQueryset, Event, Speaker, StreamPage


def redirect_speakers(request, slug):
    speaker = get_object_or_404(Speaker, wordpress_url=slug)
    return redirect(speaker.get_url(), permanent=True)


def redirect_events(request, slug):
    event = get_object_or_404(Event, wordpress_url=slug)
    return redirect(event.get_url(), permanent=True)


def redirect_wagtail_events(request, event_id, slug):
    return redirect(f"/bhd/events/{event_id}/{slug}")


def redirect_wagtail_speakers(request, slug):
    return redirect(f"/bhd/speakers/{slug}")


def handler404(request, exception):
    # capture_message(f"Error 404 {request.path}")
    return page_not_found(request, exception)


def choose_language(request, lang_code):
    next_url = request.META.get("HTTP_REFERER") or "/"

    response = HttpResponseRedirect(next_url)
    if lang_code and check_for_language(lang_code):
        parsed = urlsplit(next_url)
        new_path = f"/{lang_code}/" + parsed.path[4:]
        next_url = urlunsplit(
            (parsed.scheme, parsed.netloc, new_path, parsed.query, parsed.fragment)
        )
        response = HttpResponseRedirect(next_url)
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
    return response


def stream_api(request):
    page = StreamPage.objects.only("live_revision_id").last()
    return JsonResponse({"live_revision": page.live_revision_id})


def archive_api(request):
    """Used only for debugging SQL performance"""
    qs = ArchiveQueryset()
    events = str(qs.json())
    return HttpResponse(f"<html><body>{events}</body></html>")
