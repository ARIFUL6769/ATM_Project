from django.shortcuts import render, redirect
from .models import Account
from decimal import Decimal, InvalidOperation
from django.db import transaction
from .models import Account, TransferTransaction
from django.db import models
from django.contrib import messages


# login page
def index(request):

    if request.method == "POST":
        account_number = request.POST.get("account_number")
        pin = request.POST.get("password")

        try:
            account = Account.objects.get(account_number=account_number)

            if account.pin == pin:
                request.session["account_number"] = account.account_number

                return redirect("login")

            else:
                return render(
                    request, "index.html", {"pin_error": "PIN does not match."}
                )

        except Account.DoesNotExist:
            return render(
                request, "index.html", {"pin_error": "Account Number not found."}
            )
    return render(request, "index.html")


# about page
def about(request):
    return render(request, "about.html")


# account information page
def Account_Information(request):
    return render(request, "Account_information.html")


def contact(request):
    return render(request, "contact.html")


def privacy(request):
    return render(request, "privacy.html")


# Change PIN
def change_pin(request):

    return render(request, "change_pin.html")


# create account page
def create_account(request):
    if request.method == "POST":
        full_name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        account_number = request.POST.get("account_number")
        pin = request.POST.get("pin")
        confirm_pin = request.POST.get("confirm_pin")
        if Account.objects.filter(email=email).exists():
            return render(
                request,
                "create_acc.html",
                {"error": "This email is already registered."},
            )

        if Account.objects.filter(email=email).exists():
            return render(
                request,
                "create_acc.html",
                {"error": "This email address is already registered."},
            )

        # Check PIN
        if pin != confirm_pin:
            return render(
                request,
                "create_acc.html",
                {"error": "PIN and Confirm PIN do not match."},
            )

        # Save account information
        Account.objects.create(
            full_name=full_name,
            address=address,
            phone=phone,
            email=email,
            account_number=account_number,
            pin=pin,
        )

        return redirect("index")
    return render(request, "create_acc.html")


def deposit(request):
    account_number = request.session.get("account_number")

    if not account_number:
        return redirect("index")

    account = Account.objects.get(account_number=account_number)

    if request.method == "POST":
        try:
            amount = Decimal(request.POST.get("amount", ""))

            if not amount.is_finite() or amount <= 0:
                raise ValueError

            account.balance += amount
            account.save()

            return render(
                request,
                "deposit.html",
                {"message": "Deposit successful!", "balance": account.balance},
            )

        except (InvalidOperation, ValueError, TypeError):
            return render(
                request,
                "deposit.html",
                {
                    "error": "Please enter a valid positive amount.",
                    "balance": account.balance,
                },
            )

    return render(request, "deposit.html", {"balance": account.balance})


def withdraw(request):
    account_number = request.session.get("account_number")

    if not account_number:
        return redirect("index")

    account = Account.objects.get(account_number=account_number)

    if request.method == "POST":
        try:
            amount = Decimal(request.POST.get("amount", ""))

            if not amount.is_finite() or amount <= 0:
                raise ValueError

            if amount > account.balance:
                return render(
                    request,
                    "withdraw.html",
                    {"error": "Insufficient balance!", "balance": account.balance},
                )

            account.balance -= amount
            account.save()

            return render(
                request,
                "withdraw.html",
                {"message": "Withdrawal successful!", "balance": account.balance},
            )

        except (InvalidOperation, ValueError, TypeError):
            return render(
                request,
                "withdraw.html",
                {
                    "error": "Please enter a valid positive amount.",
                    "balance": account.balance,
                },
            )

    return render(request, "withdraw.html", {"balance": account.balance})


def transfer(request):
    account_number = request.session.get("account_number")

    if not account_number:
        return redirect("login")

    if request.method == "POST":
        recipient_number = request.POST.get("recipient_number", "").strip()

        try:
            amount = Decimal(request.POST.get("amount", ""))

            if not amount.is_finite() or amount <= 0:
                raise ValueError

        except (InvalidOperation, ValueError, TypeError):
            account = Account.objects.get(account_number=account_number)
            return render(
                request,
                "Transfer.html",
                {
                    "balance": account.balance,
                    "error": "Please enter a valid positive amount.",
                },
            )

        if recipient_number == account_number:
            account = Account.objects.get(account_number=account_number)
            return render(
                request,
                "Transfer.html",
                {
                    "balance": account.balance,
                    "error": "You cannot transfer money to your own account.",
                },
            )

        try:
            with transaction.atomic():
                sender = Account.objects.select_for_update().get(
                    account_number=account_number
                )
                recipient = Account.objects.select_for_update().get(
                    account_number=recipient_number
                )

                if amount > sender.balance:
                    return render(
                        request,
                        "Transfer.html",
                        {"balance": sender.balance, "error": "Insufficient balance!"},
                    )

                sender.balance -= amount
                recipient.balance += amount

                sender.save()
                recipient.save()
                TransferTransaction.objects.create(
                    sender=sender, recipient=recipient, amount=amount
                )

            return render(
                request,
                "Transfer.html",
                {"balance": sender.balance, "message": "Transfer successful!"},
            )

        except Account.DoesNotExist:
            account = Account.objects.get(account_number=account_number)
            return render(
                request,
                "Transfer.html",
                {"balance": account.balance, "error": "Recipient account not found."},
            )

    account = Account.objects.get(account_number=account_number)

    return render(request, "Transfer.html", {"balance": account.balance})


def transfer_history(request):
    account_number = request.session.get("account_number")

    if not account_number:
        return redirect("index")

    try:
        account = Account.objects.get(account_number=account_number)
    except Account.DoesNotExist:
        request.session.flush()
        return redirect("index")

    history = (
        TransferTransaction.objects.filter(
            models.Q(sender=account) | models.Q(recipient=account)
        )
        .select_related("sender", "recipient")
        .order_by("-created_at")
    )

    return render(request, "transfer_history.html", {"history": history})


def logout(request):
    return render(request, "logout.html")


def login(request):
    return render(request, "login.html")


def check_balance(request):
    account_number = request.session.get("account_number")
    print("Account Number from session:", account_number)
    if not account_number:
        return redirect("index")
    account = Account.objects.get(account_number=account_number)

    try:
        account = Account.objects.get(account_number=account_number)
    except Account.DoesNotExist:
        return redirect("index")

    return render(request, "balance.html", {"check_balance": account.balance})
