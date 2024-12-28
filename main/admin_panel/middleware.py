from django.shortcuts import redirect
from django.urls import resolve, reverse_lazy


class AdminPanelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Resolve the current app and URL name
        resolver = resolve(request.path_info)
        current_app = resolver.app_name or ""
        current_url_name = resolver.url_name or ""

        if current_app != "admin_panel":
            return self.get_response(request)

        if current_url_name in ("admin_login", "admin_otp_check"):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect("admin_login")

        if not request.user.is_staff:
            return redirect(reverse_lazy("home"))

        return self.get_response(request)
