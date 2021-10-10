import time

from django.utils.http import http_date


def logged_in_middleware(get_response):
    """Set cookie after user logs in. This is used later in JS to show
    Wagtail's userbar only to authenticated users.
    """

    def middleware(request):
        response = get_response(request)

        if request.path == "/admin/login/" and request.user.is_authenticated:
            # copied from SessionMiddleware
            max_age = request.session.get_expiry_age()
            expires_time = time.time() + max_age
            expires = http_date(expires_time)

            response.set_cookie("user_logged_in", expires=expires)
        return response

    return middleware
