from django.shortcuts import render


# ---------------------------------------------------------------------
def bank_carts(request):
    if not request.method == "POST":
        return render(request, "website/panel/bank-carts.html")
    return render(request, "website/panel/bank-carts.html")


# ---------------------------------------------------------------------
def edit_bank_cart(request):
    if not request.method == "POST":
        return render(request, "website/panel/bank-cart-edit.html")
    return render(request, "website/panel/bank-cart-edit.html")


# ---------------------------------------------------------------------
def create_bank_cart(request):
    if not request.method == "POST":
        return render(request, "website/panel/bank-cart-create.html")
    return render(request, "website/panel/bank-cart-create.html")
