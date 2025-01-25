from django.shortcuts import redirect
from django.urls import resolve, reverse_lazy


class AdminLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Resolve the current app and URL name
        resolver = resolve(request.path_info)
        path = request.path
        current_url_name = resolver.url_name or ""

        if current_url_name in (
            "admin_login",
            "admin_otp_check",
        ) or not path.startswith("/website-manager/"):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect("admin_login")

        if not request.user.is_staff:
            return redirect(reverse_lazy("home"))

        return self.get_response(request)
