from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages


# Create your views here.
def index(request):
    try:
        del request.session['loggedInUserID']
    except KeyError:
        pass
    return render(request, 'loginRegApp/index.html', {})


def createuser(request):
    # print(request.POST)
    first_name = request.POST['fname']
    last_name = request.POST['lname']
    email = request.POST['email']
    password = request.POST['pwd']

    validation_errors = User.objects.registration_validator(request.POST)

    if validation_errors:
        for key, value in validation_errors.items():
            messages.error(request, value)
        return redirect('loginRegApp:index')
    else:
        newuser = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password) # Never save password(s) as plain text
        )
        messages.success(
            request, f'User with email: \"{email}\" created successfully')
        request.session['loggedInUserID'] = newuser.id
        return redirect('loginRegApp:success')


def loginuser(request):
    # print(request.POST)
    email = request.POST['email_login']
    password = request.POST['pwd_login']

    validation_errors = User.objects.login_validator(request.POST)

    if validation_errors:
        for key, value in validation_errors.items():
            messages.error(request, value)
        return redirect('loginRegApp:index')

    else:
        user = User.objects.filter(
            email=email,
        ).first()

        password_from_db = user.password

        valid_user = check_password(password, password_from_db)

        if valid_user:
            messages.success(
                request, f'User with email: \"{email}\" logged in successfully')
            request.session['loggedInUserID'] = user.id
            return redirect('loginRegApp:success')

        else:
            messages.error(request, 'Credentials incorrect')
            return redirect('loginRegApp:index')


def success(request):
    id = request.session.get('loggedInUserID')
    if id:
        user = get_object_or_404(User, id=id)
        return render(request, 'loginRegApp/success.html', {'user': user})
    return redirect('loginRegApp:index')


def logoutuser(request):
    request.session.clear()
    return redirect('loginRegApp:index')
