from django.shortcuts import render, redirect
from django.contrib import messages


def addresses(request):
    return render(
        request, "user_panel/address/addresses.html", {"section": "addresses"}
    )


def update_address(request):
    return render(
        request,
        "user_panel/address/address-form.html",
        {"section": "addresses"},
    )
