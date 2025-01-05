from django.shortcuts import render


# ---------------------------------------------------------------------
def alerts(request):
    if not request.method == "POST":
        return render(request, "website/panel/alerts.html")
    return render(request, "website/panel/alerts.html")


# ---------------------------------------------------------------------
def alert_detail(request):
    if not request.method == "POST":
        return render(request, "website/panel/alert-detail.html")
    return render(request, "website/panel/alert-detail.html")
