from home.models import FestivalPage


def festival_finder(request):
    festival_slugs = set(FestivalPage.objects.values_list("slug", flat=True))
    url_parts = request.path.split("/")
    first_url_part = url_parts[2] if len(url_parts) > 2 else ""
    if first_url_part in festival_slugs:
        festival = FestivalPage.objects.get(slug=first_url_part)
    else:
        festival = FestivalPage.objects.get(slug="bhd")
    return {"festival": festival}
