class FixUrlMixin:
    """This is to quick fix to handle new wagtail i18n problem
    https://github.com/wagtail/wagtail/issues/6531
    """
    def get_url_parts(self, request=None):
        site_id, root_url, page_path = super().get_url_parts(request)
        if page_path.startswith("/sk-sk/"):
            page_path = f"/sk/{page_path[7:]}"
        return site_id, root_url, page_path

