from django.shortcuts import render


# ---------------------------------------------------------------------
def addresses(request):
    if not request.method == "POST":
        return render(request, "website/panel/addresses.html")
    return render(request, "website/panel/addresses.html")


# ---------------------------------------------------------------------
def edit_address(request):
    if not request.method == "POST":
        return render(request, "website/panel/address-edit.html")
    return render(request, "website/panel/address-edit.html")


# ---------------------------------------------------------------------
def create_address(request):
    if not request.method == "POST":
        return render(request, "website/panel/address-create.html")
    return render(request, "website/panel/address-create.html")
