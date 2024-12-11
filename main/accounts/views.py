from django.shortcuts import render


def login(request):
    return render(request, "website/login.html")


def login_otp(request):
    return render(request, "website/otp-sms.html")
