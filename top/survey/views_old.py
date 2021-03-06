from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import ListView

from .models import Client, Query, Contact, Item, ClientChange
from .forms import LoginForm, ClientsSortingForm, QuerySortingForm, ClientInfoForm


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
    return render(request, 'main.html', {'user': user})


# lists-----------------------------------------------------------------------------------------------------------------


class ClientsList(ListView):

    template_name = 'clients.html'
    model = Client

    def dispatch(self, request, *args, **kwargs):
        self.form = ClientsSortingForm(request.GET)
        self.form.is_valid()
        self.user = request.user
        return super(ClientsList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Client.objects.all()
        if is_manager(self.user):
            queryset = queryset.filter(manager_id=self.user)
        if self.form.cleaned_data.get('search'):
            queryset = queryset.filter(name__icontains=self.form.cleaned_data.get('search'))
        if self.form.cleaned_data.get('sort_by'):
            queryset = queryset.order_by(self.form.cleaned_data.get('sort_by'))
        if self.form.cleaned_data.get('filter'):
            queryset = queryset.order_by(self.form.cleaned_data.get('sort_by'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ClientsList, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context


def client(request, num):
    c = get_object_or_404(Client, id=num)
    changes = ClientChange.objects.filter(client=c)
    return render(request, 'client_detail.html', {'client': c,
                                                  'changes': changes})


def client_hist(request, num):
    c = get_object_or_404(Client, id=num)
    changes = ClientChange.objects.all()
    return render(request, 'client_hist.html', {'client': c,
                                                  'changes': changes})


def client_info_form_view(request, num):
    client = Client.objects.get(pk=num)
    if request.method == "POST":
        form = ClientInfoForm(request.POST)
        if form.is_valid():
            c = ClientInfoForm(request.POST, instance=client)
            c.save()
            client.basic_survey = True
            client.save()
            return HttpResponseRedirect('/clients/'+num+'/')
    else:
        form = ClientInfoForm()
    return render(request, 'client_info_form.html', {'form': form,
                                                     'user': request.user,
                                                     'session': request.session, })


def client_info_edit(request, num):
    c = Client.objects.get(pk=num)
    old = {'type': c.type,
           'sanctions': c.sanctions,
           'crimea': c.crimea,
           'imp': c.imp}
    if request.method == "POST":
        form = ClientInfoForm(request.POST, instance=c)
        if form.is_valid():
            fields = ['type', 'sanctions', 'crimea', 'imp']
            for i in fields:
                if old.get(i) != request.POST.get(i):
                    change = ClientChange()
                    change.change = old.get(i) + ' => ' + form.cleaned_data.get(i)
                    change.field = i
                    change.manager = request.user
                    change.client = c
                    change.save()
            form.save()
            return HttpResponseRedirect('/clients/'+num+'/')
    else:
        form = ClientInfoForm(initial={'type': c.type,
                                       'sanctions': c.sanctions,
                                       'crimea': c.crimea,
                                       'imp': c.imp})
    return render(request, 'client_info_form.html', {'form': form,
                                                     'user': request.user,
                                                     'session': request.session, })



class QueryList(ListView):

    template_name = 'queries.html'
    model = Query

    def dispatch(self, request, *args, **kwargs):
        self.form = QuerySortingForm(request.GET)
        self.form.is_valid()

    def get_queryset(self):
        queryset = Query.objects.all()
        if self.form.cleaned_data.get('search'):
            queryset = queryset.filter(name__contains=self.form.cleaned_data.get('search'))
        if self.form.cleaned_data.get('sort_by'):
            queryset = queryset.order_by(self.form.cleaned_data.get('sort_by'))
        if self.form.cleaned_data.get('only_open'):
            queryset = queryset.filter(status_in=['query','lead','order'])
            return queryset

    def get_context_data(self, **kwargs):
            context = super(QueryList, self).get_context_data(**kwargs)
            context['form'] = self.forms

