from django.db.models import OuterRef, Subquery, ExpressionWrapper, Count, IntegerField
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import ListView, CreateView, DeleteView
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Client, Query, Person, Item, ClientChange
from .forms import LoginForm, ClientsSortingForm, QuerySortingForm, ClientInfoForm, QueryForm, AddClientForm, AddContactForm


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
        open_st = [u'Запрос', u'Лид', u'Заявка']
        queryset = queryset.annotate(open_query=Count(Subquery(Query.objects.filter(client=OuterRef('pk'), status__in=open_st).values('pk'))))
        queryset = queryset.order_by('-open_query')
        if is_manager(self.user):
            queryset = queryset.filter(manager_id=self.user)
        if self.form.cleaned_data.get('search'):
            queryset = queryset.filter(name__icontains=self.form.cleaned_data.get('search'))
        if self.form.cleaned_data.get('sort_by'):
            queryset = queryset.order_by(self.form.cleaned_data.get('sort_by'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ClientsList, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context


class AddClient(CreateView):

    form_class = AddClientForm
    model = Client
    template_name = 'client_add.html'

    def form_valid(self, form):
        if is_manager(self.request.user):
            form.instance.manager = self.request.user
        return super(AddClient, self).form_valid(form)


def add_client(request):
    if request.method == 'POST':
        client_form = AddClientForm(request.POST)
        contact_form = AddContactForm(request.POST)
        if client_form.is_valid() and contact_form.is_valid():
            client = client_form.save()
            client.manager = request.user
            client.save()
            contact = contact_form.save()
            contact.client = client
            return HttpResponseRedirect('/clients/'+str(client.pk)+'/')
    else:
        client_form = AddClientForm()
        contact_form = AddContactForm()
        return render(request, 'client_add.html', {'form1': client_form,
                                                   'form2': contact_form
                                                   })


class ClientDelete(DeleteView):

    model = Client
    success_url = '/clients/'


class AddContact(CreateView):

    form_class = AddContactForm
    model = Person
    template_name = 'client_add_contact.html'

    def dispatch(self, request, *args, **kwargs):
        self.client = get_object_or_404(Client, pk=self.kwargs['num'])
        return super(AddContact, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        contact = form.save()
        contact.client = self.client
        return super(AddContact, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddContact, self).get_context_data(**kwargs)
        context['client'] = self.client
        return context


def client_detail(request, num):
    c = get_object_or_404(Client, id=num)
    changes = ClientChange.objects.filter(client=c)
    contact = Person.objects.filter(client=c)
    return render(request, 'client_detail.html', {'client': c,
                                                  'changes': changes,
                                                  'contacts': contact,
                                                  })


def client_hist(request, num, ch=None):

    template_name = 'client_hist.html'

    c = get_object_or_404(Client, id=num)
    changes = ClientChange.objects.filter(client=c)
    old = ch
    if old is not None:
        old = get_object_or_404(ClientChange, id=ch)
        template_name = 'hist_old.html'
    return render(request, template_name, {'client': c,
                                           'changes': changes,
                                           'old': old})


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
            msg = ''
            for i in fields:
                if old.get(i) != form.cleaned_data.get(i):
                    msg += 'Изменено поле "' + c._meta.get_field(i).verbose_name + '":' + old.get(i) + ' => ' + form.cleaned_data.get(i) + '\n'
            if msg != '':
                change = ClientChange(type=old.get('type'), sanctions=old.get('sanctions'), crimea=old.get('crimea'), imp=old.get('imp'))
                change.change = msg
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
        self.user = request.user
        return super(QueryList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Query.objects.all()
        if self.form.cleaned_data.get('search'):
            queryset = queryset.filter(name__icontains=self.form.cleaned_data.get('search'))
        if self.form.cleaned_data.get('sort_by'):
            queryset = queryset.order_by(self.form.cleaned_data.get('sort_by'))
        if self.form.cleaned_data.get('only_open'):
            queryset = queryset.filter(status__in=['query', 'lead', 'order'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(QueryList, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context


def new_query(request, num):
    if request.method == "POST":
        client = Client.objects.get(pk=num)
        manager = request.user
        query = Query(client=client, manager=manager, status=u'Запрос')
        form = QueryForm(request.POST, instance=query)
        if form.is_valid():
            name = u'Заказ на ' + form.cleaned_data.get('product_type') + u' от ' + datetime.datetime.today().strftime("%d.%m.%Y")
            query.name = name
            query.survey = True
            form.save()
            url = str(query.pk) + '/'
            return HttpResponseRedirect(url)
    else:
        form = QueryForm()
        return render(request, 'query_form.html', {'form': form})


def item_list(request, num, qnum):
    query = Query.objects.get(pk=qnum)
    client = Client.objects.get(pk=num)
    qs = Item.objects.filter(product_type=query.product_type,
                             form_factor=query.form_factor,
                             type=query.type,
                             upgrade=query.upgrade
                             )
    total, one, more = {}, {}, {}
    for obj in qs:
        dif = []
        k = 0
        if obj.certificate != query.certificate:
            k += 1
            dif.append(u'Сертификация')
        if obj.price_bracket != query.fav_brands:
            k += 1
            dif.append(u'Ценовая категория')
        if obj.imp != client.imp:
            k += 1
            dif.append(u'Импортозамещение')
        if obj.sanctions != client.sanctions:
            k += 1
            dif.append(u'Санкции')
        if obj.crimea != client.crimea:
            k += 1
            dif.append(u'Крым')

        if k == 0:
            total[obj.id] = str(dif)
        if k == 1:
            one[obj.id] = str(dif)
        if k > 1:
            more[obj.id] = str(dif)

    tot = qs.filter(id__in=total.keys())
    on = qs.filter(id__in=one.keys())
    mor = qs.filter(id__in=more.keys())

    return HttpResponse(on)
    return render(request, 'query_result_list.html', {'total': tot,
                                                      'one': on,
                                                      'more': mor,
                                                      'query': query,
                                                      'client': client,
                                                      }
                  )

