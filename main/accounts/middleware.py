from django.shortcuts import redirect
from django.urls import resolve


class CustomerLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Resolve the current app and URL name
        resolver = resolve(request.path_info)
        path = request.path
        current_url_name = resolver.url_name or ""

        if current_url_name in (
            "customer_login",
            "customer_otp_check",
        ) or not (path.startswith("/auth/") or path.startswith("/user/")):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect("customer_login")

        return self.get_response(request)
