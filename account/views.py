from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from post.models import BlogPost


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            account = authenticate(email=email, password=raw_password, first_name=first_name, last_name=last_name)
            login(request, account)
            return redirect('home-url')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home-url')


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home-url')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home-url')

    else:
        form = AccountAuthenticationForm()

        context = {}
        context['login_form'] = form
        return render(request, 'account/login.html', context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login-url')
    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    context['account_form'] = form
    blog_posts = BlogPost.objects.filter()
    context['blog_posts'] = blog_posts
    return render(request, 'account/profile.html', context)


def must_authenticate(request):
    return render(request, 'account/must_authenticate.html')
