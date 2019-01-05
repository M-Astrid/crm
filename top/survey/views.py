from django.db.models import OuterRef, Subquery, Count, F, CharField, ExpressionWrapper, Value, IntegerField
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
import datetime


from .models import Client, Query, Person, Item, ClientChange, PersonChange
from .forms import LoginForm, ClientsSortingForm, QuerySortingForm, ClientInfoForm, QueryForm, AddClientForm, \
    AddContactForm, DeclineForm


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

        queries = Query.objects.filter(client=OuterRef('pk'), status__in=open_st).order_by().values('client')
        count_queries = queries.annotate(c=Count('pk', output_field=IntegerField())).values('c')
        open_query = Subquery(count_queries, output_field=IntegerField())
        queryset = queryset.annotate(open_query=open_query)

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


def client_info_edit(request, num):

    c = Client.objects.get(pk=num)
    dict = model_to_dict(c)
    fields = ['type', 'sanctions', 'crimea', 'imp']
    old = {}
    for i in fields:
        old[i] = dict.get(i)

    if request.method == "POST":
        form = ClientInfoForm(request.POST, instance=c)
        if form.is_valid():
            msg = ''
            for i in fields:
                if old.get(i) != form.cleaned_data.get(i):
                    msg += 'Изменено поле "' + c._meta.get_field(i).verbose_name + '":' + old.get(i) + ' => ' + form.cleaned_data.get(i) + '\n'
            if msg != '':
                change = ClientChange(type=old.get('type'), sanctions=old.get('sanctions'), crimea=old.get('crimea'), imp=old.get('imp'))
                change.change = msg
                change.ch_type = 'Базовый опрос'
                change.manager = request.user
                change.client = c
                change.save()
                form.save()
            #return HttpResponse(ol.get('type'))
            return HttpResponseRedirect('/clients/'+num+'/')
    else:
        form = ClientInfoForm(initial=old)
    return render(request, 'client_info_form.html', {'form': form,
                                                     'user': request.user,
                                                     'session': request.session, })


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
        contact = form.save(commit=False)
        contact.client = self.client
        if form.is_valid():
            msg = 'Добавлено контактное лицо ' + form.cleaned_data.get('last_name') + ' ' + form.cleaned_data.get('first_name')
            change = ClientChange()
            change.ch_type = 'Контактные лица'
            change.change = msg
            change.manager = self.request.user
            change.client = self.client
            change.save()
            form.save()
            return HttpResponseRedirect("/clients/%i/" % self.client.pk)

    def get_context_data(self, **kwargs):
        context = super(AddContact, self).get_context_data(**kwargs)
        context['client'] = self.client
        return context


class EditContact(UpdateView):

    model = Person
    template_name = 'client_add_contact.html'

    def dispatch(self, request, *args, **kwargs):
        self.person = get_object_or_404(Person, pk=self.kwargs['pk'])
        self.client = get_object_or_404(Client, pk=self.kwargs['num'])
        dict = model_to_dict(self.person)
        self.fields = ['last_name', 'first_name', 'father_name', 'phone_number', 'phone_number2', 'email', 'position']
        self.old = {}
        for i in self.fields:
            self.old[i] = dict.get(i)
        return super(EditContact, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            msg = 'У контактного лица ' + self.person.last_name + ' ' + self.person.first_name + ' '
            for i in self.fields:
                if self.old.get(i) != form.cleaned_data.get(i):
                    msg += self.person._meta.get_field(i).verbose_name + '":' + self.old.get(
                        i) + ' => ' + form.cleaned_data.get(i) + ';\n'
            if msg != '':
                change = ClientChange(last_name=self.old.get('last_name'), first_name=self.old.get('first_name'),
                                      father_name=self.old.get('father_name'), phone_number=self.old.get('phone_number'),
                                      phone_number2=self.old.get('phone_number2'), email=self.old.get('email'),
                                      position=self.old.get('position'))
                change.change = msg
                change.ch_type = 'Контактные лица'
                change.manager = self.request.user
                change.client = self.client
                change.save()
                form.save()
                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(EditContact, self).get_context_data(**kwargs)
        context['client'] = self.client
        return context


class DeleteContact(DeleteView):

    model = Person

    def dispatch(self, request, *args, **kwargs):
        self.client = get_object_or_404(Client, pk=self.kwargs['num'])
        return super(DeleteContact, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DeleteContact, self).get_context_data(**kwargs)
        context['client'] = self.client
        person = get_object_or_404(Person, pk=self.kwargs['pk'])
        msg = 'Удалено контактное лицо ' + person.last_name + ' ' + person.first_name
        change = ClientChange(last_name=person.last_name, first_name=person.first_name,
                              father_name=person.father_name, phone_number=person.phone_number,
                              phone_number2=person.phone_number2, email=person.email,
                              position=person.position)
        change.change = msg
        change.ch_type = 'Контактные лица'
        change.manager = self.request.user
        change.client = self.client
        change.save()
        return context

    def get_success_url(self):
        url = "/clients/%i/" % self.client.pk
        return url


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
        return render(request, 'form.html', {'form': form,
                                             'title': u'Новый запрос',
                                             'button': u'Подобрать товары',
                                             })


def item_list(request, num, qnum):
    if request.method == "POST":
        checks = request.POST.getlist('checks')
        qs = Item.objects.filter(id__in=checks)
    query = Query.objects.get(pk=qnum)
    client = Client.objects.get(pk=num)
    qs = Item.objects.filter(product_type=query.product_type,
                             form_factor=query.form_factor,
                             type=query.type,
                             upgrade=query.upgrade
                             )
    total, one, more, dif1, dif2 = [], [], [], [], []
    for obj in qs:
        dif = ''
        k = 0
        if obj.certificate != query.certificate:
            k += 1
            dif += 'Сертификация '
        if obj.price_bracket != query.fav_brands:
            k += 1
            dif += 'Ценовая категория '
        if obj.imp != client.imp:
            k += 1
            dif += 'Импортозамещение '
        if obj.sanctions != client.sanctions:
            k += 1
            dif += 'Санкции '
        if obj.crimea != client.crimea:
            k += 1
            dif += 'Крым '

        if k == 0:
            total += [obj.id]
        if k == 1:
            one += [obj.id]
            dif1 += [dif]
        if k > 1:
            more += [obj.id]
            dif2 += [dif]

    tot = qs.filter(id__in=total)
    on = qs.filter(id__in=one)
    mor = qs.filter(id__in=more)

    return render(request, 'query_result_list.html', {'total': tot,
                                                      'one': on,
                                                      'more': mor,
                                                      'query': query,
                                                      'client': client,
                                                      'dif1': dif1,
                                                      'dif2': dif2,
                                                      }
                  )


def decline_order(request, pk):
    query = Query.objects.get(pk=pk)
    client = query.client
    if request.method == "POST":
        form = DeclineForm(request.POST)
        if form.is_valid():
            query.decline_reason = form.cleaned_data.get('decline_reason')
            query.status = u'Отказ'
            query.save()
            url = '/clients/%i/' % client.pk
            return HttpResponseRedirect(url)
    else:
        form = DeclineForm()
        return render(request, 'form.html', {
                                             'title': u'Отмена заказа',
                                             'button': u'Отменить заказ',
                                             'form': form,
                                             'user': request.user,
                                             'query': query,
                                             })
