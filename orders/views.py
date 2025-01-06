from django.shortcuts import render


# ---------------------------------------------------------------------
def orders(request):
    if not request.method == "POST":
        return render(request, "website/panel/orders.html")
    return render(request, "website/panel/orders.html")


# ---------------------------------------------------------------------
def order_detail(request):
    if not request.method == "POST":
        return render(request, "website/panel/order-detail.html")
    return render(request, "website/panel/order-detail.html")
