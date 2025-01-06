from django.shortcuts import render


# ---------------------------------------------------------------------
def favorites(request):
    if not request.method == "POST":
        return render(request, "website/panel/favorites.html")
    return render(request, "website/panel/favorites.html")
