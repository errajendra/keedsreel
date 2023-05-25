from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from payment.models import Transaction


""" View Transactin List. """
@login_required
def view_transaction(request):
    tnxs = Transaction.objects.all().order_by('-created_at')
    context = {
        "title": "All Transactions",
        "tnxs": tnxs
    }
    return render(request, "payments/transaction-list.html", context)
    