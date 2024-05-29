from django.contrib.auth.hashers import make_password
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# from django.utils.crypto import get_random_string

from postmarker.core import PostmarkClient

from datetime import datetime
from json import JSONEncoder
from random import SystemRandom
from string import ascii_letters, digits

from bestoon.settings import POSTMARK_API_TOKEN
from .models import Expense, Income, Token, User, Passwordresetcodes


# create random string for Token
random_str = lambda n: ''.join(
    SystemRandom().choice(ascii_letters + digits) for _ in range(n)
)

def register(request):
    if request.method == 'POST':
        if 'requestcode' in request.POST:  # form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
            # TODO: check email is not None | html required
            email = request.POST.get('email')
            username = request.POST.get('username')

            # duplicate email
            if User.objects.filter(email=email).exists():
                print(f'{User.objects.get(email=email) = }')
                context = {
                    'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده.- درست می شه',
                    'email': email if email != None else '',
                    'username': username if username != None else '',
                }  # TODO: forgot password
                # TODO: keep the form data
                return render(request, 'register.html', context)

            # if user does exist
            if User.objects.filter(username=username).exists():
                context = {
                    'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید. ببخشید که فرم ذخیره نشده. درست می شه',
                    'email': email if email != None else '',
                    'username': username if username != None else '',
                }  # TODO: forgot password
                # TODO: keep the form data
                return render(request, 'register.html', context)

            code = random_str(32)
            now = datetime.now()
            password = make_password(request.POST.get('password'))

            Passwordresetcodes.objects.create(
                email=email, time=now, code=code,
                username=username, password=password,
            )

            postmark = PostmarkClient(POSTMARK_API_TOKEN)
            body = f'''
<p>برای فعالسازی اکانت بستون خود روی لینک زیر کلیک کنید.</p>
<a href={request.build_absolute_uri(reverse('register'))}?code={code}>Confirm Bestoon Account</a>'''

            # postmark.emails.send(
            #     From='zovaruratugo@ssl.tls.cloudns.ASIA',
            #     To=email,
            #     Subject='فعالسازی اکانت بستون',
            #     HtmlBody=body,
            # )
            message = 'ایمیلی حاوی لینک فعال سازی اکانت به شما فرستاده شده، لطفا پس از چک کردن ایمیل، روی لینک کلیک کنید.'
            context = {'message': message + body}
            return render(request, 'index.html', context)

    elif request.method == 'GET':
        if 'code' in request.GET:  # user clicked on code
            code = request.GET.get('code')
            if not Passwordresetcodes.objects.filter(code=code).exists():
                context = {'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
                return render(request, 'register.html', context)
            else: # if code is in temporary db, read the data and create the user
                temp_user = Passwordresetcodes.objects.get(code=code)
                new_user = User.objects.create(
                    username=temp_user.username,
                    password=temp_user.password,
                    email=temp_user.email,
                )
                # delete the temporary activation code from db
                # Passwordresetcodes.objects.filter(code=code).delete()
                temp_user.delete()

                token = random_str(48)
                Token.objects.create(user=new_user, token=token)

                context = {
                    'message': f'اکانت شما ساخته شد. توکن شما {token} است. آن را ذخیره کنید چون دیگر نمایش داده نخواهد شد! جدی!',
                }
                return render(request, 'index.html', context)

        context = {'message': ''}
        return render(request, 'register.html', context)

    else:
        return HttpResponseBadRequest(
            f'This view can not handle method {request.method}',
            status=405,
        )
        # context = {'message': ''}
        # return render(request, 'register.html', context)

@csrf_exempt
def submit_expense(request):
    """user submits an expense"""

    # TODO: validate data. user might be fake. token might be fake. amount might be...
    this_token = request.POST.get('token')
    print(f'{this_token = }')
    this_user = User.objects.get(token__token=this_token)
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
