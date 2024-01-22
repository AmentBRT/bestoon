from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from json import JSONEncoder

from datetime import datetime

from web.models import Expense, Income, Token, User


@csrf_exempt
def submit_expense(request):
    """user submits an expense"""

    # TODO: validate data. user might be fake. token might be fake. amount might be...
    this_token = request.POST.get('token')
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()
    Expense.objects.create(
        user=this_user,
        amount=request.POST.get('amount'),
        text=request.POST.get('text'),
        date=date,
    )

    return JsonResponse({
        'status': 'ok',
    },  encoder=JSONEncoder)

@csrf_exempt
def submit_income(request):
    """user submits an income"""

    # TODO: validate data. user might be fake. token might be fake. amount might be...
    this_token = request.POST.get('token')
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()
    Income.objects.create(
        user=this_user,
        amount=request.POST.get('amount'),
        text=request.POST.get('text'),
        date=date,
    )

    return JsonResponse({
        'status': 'ok',
    },  encoder=JSONEncoder)
