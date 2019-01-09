from collections import Counter

from django.db.models import OuterRef, Subquery, Count, F, CharField, ExpressionWrapper, Value, IntegerField, Func
from .include.tools import QuerySetSequence
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
import datetime


from .models import Client, Query, Person, Item, ClientChange, PersonChange, Vendor, Certificate, PriceCat, QueryChange
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
    q_open = Query.objects.filter(client=c, status__in=[u'Запрос', u'Лид', u'Заявка'])
    q_old = Query.objects.filter(client=c, status__in=[u'Успешно реализован', u'Отказ'])
    return render(request, 'client_detail.html', {'client': c,
                                                  'changes': changes,
                                                  'contacts': contact,
                                                  'q_open': q_open,
                                                  'q_old': q_old,
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
            query = form.save()
            vendors = request.POST.getlist('checks[]')
            vendors = Vendor.objects.filter(name__in=vendors)
            certificates = request.POST.getlist('certificates[]')
            certificates = Certificate.objects.filter(name__in=certificates)
            for cert in certificates:
                query.certificate.add(cert)
            for vendor in vendors:
                query.vendors.add(vendor)
            url = '/queries/%i/' % query.pk
            #return HttpResponse(query.vendors)
            return HttpResponseRedirect(url)
    else:
        form = QueryForm()
        vendors = Vendor.objects.all()
        certificates = Certificate.objects.all()
        return render(request, 'form.html', {'form': form,
                                             'vendors': vendors,
                                             'certificates': certificates,
                                             'title': u'Новый запрос',
                                             'button': u'СОЗДАТЬ ЗАПРОС',
                                             })


class QueryUpdate(UpdateView):

    model = Query
    template_name = 'form.html'

    def dispatch(self, request, *args, **kwargs):
        self.query = get_object_or_404(Query, pk=self.kwargs['pk'])
        dict = model_to_dict(self.query)
        self.fields = ['product_type', 'form_factor', 'type', 'upgrade']
        self.f2 = 'certificate'
        self.old = {}
        for i in self.fields:
            self.old[i] = dict.get(i)
        self.old[self.f2] = dict.get(self.f2)
        self.form = QueryForm(initial=dict, instance=self.query)
        return super(QueryUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            msg = ''
            certificates = self.request.POST.getlist('certificates[]')
            certificates = Certificate.objects.filter(name__in=certificates)
            for i in self.fields:
                if self.old.get(i) != form.cleaned_data.get(i):
                    msg += u'Изменен параметр ' + self.query._meta.get_field(i).verbose_name + '":' + self.old.get(
                        i) + ' => ' + form.cleaned_data.get(i) + ';\n'
            if self.old.get(self.f2) != certificates:
                msg += u'Изменен параметр "Сертификат": '
                l = len(self.old.get(self.f2))
                c = 0
                for i in self.old.get(self.f2):
                    msg += i.name
                    c += 1
                    if c != l:
                        msg += ', '
                msg += ' => '
                l = len(certificates)
                c = 0
                for i in certificates:
                    msg += i.name
                    c += 1
                    if c != l:
                        msg += ', '
                msg += ';\n'
            if msg != '':
                change = QueryChange()
                change.change = msg
                change.manager = self.request.user
                change.query = self.query
                change.save()
                query = form.save()
                query.certificate.clear()
                for cert in certificates:
                    query.certificate.add(cert)
                vendors = self.request.POST.getlist('checks[]')
                vendors = Vendor.objects.filter(name__in=vendors)
                query.vendors.clear()
                for vendor in vendors:
                    query.vendors.add(vendor)
                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(QueryUpdate, self).get_context_data(**kwargs)
        context['button'] = 'Применить'
        context['title'] = 'Изменить условия запроса'
        context['vendors'] = Vendor.objects.all()
        context['certificates'] = Certificate.objects.all()
        return context


def query_changes(request, pk):
    query = get_object_or_404(Query, pk=pk)
    changes = QueryChange.objects.filter(query=query).order_by('-id')
    client = query.client
    return render(request, 'query_history.html', {
        'changes': changes,
        'user': request.user,
        'client': client,
        'query': query,
    })


def item_list(request, pk):
    query = Query.objects.get(pk=pk)
    client = query.client
    if request.method == "POST":
        checks = request.POST.getlist('checks[]')
        if checks:
            qs = Item.objects.filter(id__in=checks)
            for i in qs:
                query.lead_items.add(i)
            return HttpResponseRedirect('lead')
    else:
        qs = Item.objects.filter(product_type=query.product_type,
                                 form_factor=query.form_factor,
                                 type=query.type,
                                 upgrade=query.upgrade
                                 )
        certs = query.certificate.all()
        q_certs = []
        for cert in certs:
            q_certs.append(cert.name)

        q_vends = query.vendors.all()

        #qs = qs.filter(pk=7)

        total, vopr, one, more, dif1, dif2 = [], [], [], [], [], []
        for obj in qs:
            dif = ''
            k = 0
            v = 0
            c = 0
            if obj.eac == u'+' and u'EAC' in q_certs:
                c += 1
            if obj.ST1 == u'+' and u'СТ1' in q_certs:
                c += 1
            if obj.torp == u'+' and u'ТОРП' in q_certs:
                c += 1
            if not c:
                if obj.eac == u'?' and u'EAC' in q_certs:
                    v += 1
                elif obj.ST1 == u'?' and u'СТ1' in q_certs:
                    v += 1
                elif obj.torp == u'?' and u'ТОРП' in q_certs:
                    v += 1
                else:
                    k += 1
                    dif += u'Сертификат '
            if obj.imp == u'?':
                v += 1
            elif obj.imp != client.imp:
                k += 1
                dif += 'Импортозамещение '

            if obj.sanctions == u'?':
                v += 1
            elif obj.sanctions != client.sanctions:
                k += 1
                dif += 'Санкции '

            if obj.crimea == u'?':
                v += 1
            elif obj.crimea != client.crimea:
                k += 1
                dif += 'Крым '

            if k == 0 and not v:
                total += [obj.id]
            if k == 0 and v:
                vopr += [obj.id]
            if k == 1:
                one += [obj.id]
                dif1 += [dif]
            if k > 1:
                more += [obj.id]
                #dif2 += [dif]
        vends = []
        for v in q_vends:
            vends.append(v.price_cat)
        d = [[vends.count(1), 1], [vends.count(2), 2], [vends.count(3), 3]]
        d = sorted(d)

        if d[2][1] == 1 and d[1][0] == d[0][0]:
            d[1][1] = 2
            d[0][1] = 3
        if d[2][1] == 3 and d[1][0] == d[0][0]:
            d[1][1] = 2
            d[0][1] = 1
        if d[2][0] == d[1][0] == d[0][0]:
            d[2][1] = 1
            d[1][1] = 2
            d[0][1] = 3

        tot = qs.filter(id__in=total)
        tot1 = tot.filter(price_bracket=d[2][1])
        tot2 = tot.filter(price_bracket=d[1][1])
        tot3 = tot.filter(price_bracket=d[0][1])

        vop = qs.filter(id__in=vopr)

        vop1 = vop.filter(price_bracket=d[2][1])
        vop2 = vop.filter(price_bracket=d[1][1])
        vop3 = vop.filter(price_bracket=d[0][1])

        on = qs.filter(id__in=one)

        on1 = on.filter(price_bracket=d[2][1])
        on2 = on.filter(price_bracket=d[1][1])
        on3 = on.filter(price_bracket=d[0][1])

        mor = qs.filter(id__in=more)

        mor1 = mor.filter(price_bracket=d[2][1])
        mor2 = mor.filter(price_bracket=d[1][1])
        mor3 = mor.filter(price_bracket=d[0][1])

        #return HttpResponse(q_certs)
        return render(request, 'query_result_list.html', {'tot': [tot1, tot2, tot3],
                                                          'vop': [vop1, vop2, vop3],
                                                          'on': [on1, on2, on3],
                                                          'mor': [mor1, mor2, mor3],
                                                          'client': client,
                                                          'test': qs,
                                                          'query': query,
                                                          'dif1': dif1,
                                                          #'dif2': dif2,
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
