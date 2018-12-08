from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm
from .models import Client, Query, Contact, Item


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            print(username, password)
            user = authenticate(username=username, password=password)
            print(type(user))
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/main')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form,
                                          'user': request.user,
                                          'session': request.session, })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')


