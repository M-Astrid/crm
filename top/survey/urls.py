from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'survey'

urlpatterns = [
    url(r'^$', views.main),
    url(r'^main/', views.main),
    url(r'^login/', views.login_view),
    url(r'^logout/', views.logout_view),
    url(r'^clients/', login_required(views.ClientsList.as_view(template_name="clients.html"))),
]
