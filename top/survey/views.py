from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView

from .models import Client, Query, Contact, Item
from .forms import ClientsSortingForm

from .forms import LoginForm


# auth_views------------------------------------------------------------------------------------------------------------

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
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form,
                                          'user': request.user,
                                          'session': request.session, })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')


# permissions checks----------------------------------------------------------------------------------------------------

def is_manager(user):
    return user.groups.filter(name='manager').exists()


def is_admin(user):
    return user.groups.filter(name='admin').exists()


def main(request):
    user = request.user
    return render(request, 'main.html', {'user': user })


# lists-----------------------------------------------------------------------------------------------------------------


class ClientsList(ListView):

    template_name = 'clients.html'
    model = Client
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        self.form = ClientsSortingForm(request.GET)
        self.form.is_valid()
        return super(ClientsList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Client.objects.all()
        if self.form.cleaned_data.get('search'):
            queryset = queryset.filter(name__icontains=self.form.cleaned_data.get('search'))
        if self.form.cleaned_data.get('sort_by'):
            queryset = queryset.order_by(self.form.cleaned_data.get('sort_by'))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ClientsList, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

