from django.contrib import admin

# Register your models here.
from .models import Client, Contact, Query, Item

for i in [Client, Contact, Query, Item]:
    admin.site.register(i)
