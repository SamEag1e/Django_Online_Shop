from django.shortcuts import render


# ---------------------------------------------------------------------
def tickets(request):
    if not request.method == "POST":
        return render(request, "website/panel/tickets.html")
    return render(request, "website/panel/tickets.html")


# ---------------------------------------------------------------------
def ticket_detail(request):
    if not request.method == "POST":
        return render(request, "website/panel/ticket-detail.html")
    return render(request, "website/panel/ticket-detail.html")


# ---------------------------------------------------------------------
def create_ticket(request):
    if not request.method == "POST":
        return render(request, "website/panel/ticket-create.html")
    return render(request, "website/panel/ticket-create.html")
