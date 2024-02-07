from django.http import HttpResponse
from django.shortcuts import render, redirect
from subscription.models import Subscription
from .credentials import *
from .forms import SubscribeForm
from django.contrib import messages


def add_subscription(request):
    if request.POST:
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Amount added successfully')
            return redirect('home-url')
        else:
            messages.success(request, 'Failed to add amount')
    else:
        form = SubscribeForm()
    return render(request, 'subscription/add_subscription_amount.html', {'form': form})


def sub_scription_view(request):

    #cash = Subscription.objects.all()
    #context = {'cash': cash}

    if request.method == "POST":
        phone = request.POST['phone']
        amount = 1000
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "PYMENT001",
            "TransactionDesc": "School fees"
        }

        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Successful Paid")

    return render(request, 'subscription/subscribe.html')


