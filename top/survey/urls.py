from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'survey'

urlpatterns = [
    url(r'^$', login_required(views.main)),
    url(r'^main/', login_required(views.main)),
    url(r'^login/', views.login_view),
    url(r'^logout/', views.logout_view),
    url(r'^clients/$', login_required(views.ClientsList.as_view(template_name="clients.html")), name='client-list'),
    url(r'^add-client/$', login_required(views.AddClient.as_view())),
    url(r'^clients/(?P<num>[0-9]+)/$', login_required(views.client_detail), name='client_detail'),
    url(r'^clients/(?P<pk>[0-9]+)/delete/$', login_required(views.ClientDelete.as_view()), name='client-delete'),
    url(r'^clients/(?P<num>[0-9]+)/add-contact/$', login_required(views.AddContact.as_view())),
    url(r'^clients/(?P<num>[0-9]+)/(?P<pk>[0-9]+)/$', login_required(views.EditContact.as_view())),
    url(r'^clients/(?P<num>[0-9]+)/(?P<pk>[0-9]+)/delete/$', login_required(views.DeleteContact.as_view())),
    url(r'^clients/(?P<num>[0-9]+)/new-query/$', login_required(views.new_query), name='new-query'),
    url(r'^clients/(?P<num>[0-9]+)/hist_info/$', login_required(views.client_hist)),
    url(r'^clients/(?P<num>[0-9]+)/hist/$', login_required(views.client_hist)),
    url(r'^clients/(?P<num>[0-9]+)/hist/(?P<ch>[0-9]+)/$', login_required(views.client_hist)),
    url(r'^clients/(?P<num>[0-9]+)/client-info-form/$', login_required(views.client_info_form_view), name='info-form'),
    url(r'^clients/(?P<num>[0-9]+)/client-info-edit/$', login_required(views.client_info_edit), name='edit-info-form'),
    url(r'^queries/$', login_required(views.QueryList.as_view(template_name="queries.html"))),
    url(r'^queries/(?P<pk>[0-9]+)/$', login_required(views.item_list), name='item-list'),
    url(r'^queries/(?P<pk>[0-9]+)/edit/$', login_required(views.QueryUpdate.as_view())),
    url(r'^queries/(?P<pk>[0-9]+)/history/$', login_required(views.query_changes)),
    url(r'^queries/(?P<pk>[0-9]+)/decline/$', login_required(views.decline_order)),
]
