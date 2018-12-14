from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'survey'

urlpatterns = [
    url(r'^$', login_required(views.main)),
    url(r'^main/', login_required(views.main)),
    url(r'^login/', views.login_view),
    url(r'^logout/', views.logout_view),
    url(r'^clients/$', login_required(views.ClientsList.as_view(template_name="clients.html"))),
    url(r'^clients/(?P<num>[0-9]+)/$', login_required(views.client), name='client-detail'),
    url(r'^clients/(?P<num>[0-9]+)/new-query/$', login_required(views.client), name='client-detail'),
    url(r'^clients/(?P<num>[0-9]+)/hist/$', login_required(views.client_hist), name='client-detail'),
    url(r'^clients/(?P<num>[0-9]+)/hist/(?P<ch>[0-9]+)/$', login_required(views.client_hist), name='client-detail'),
    url(r'^clients/(?P<num>[0-9]+)/client-info-form/', login_required(views.client_info_form_view), name='info-form'),
    url(r'^clients/(?P<num>[0-9]+)/client-info-edit/', login_required(views.client_info_edit), name='edit-info-form'),
    url(r'^queries/', login_required(views.QueryList.as_view(template_name="queries.html"))),
]
