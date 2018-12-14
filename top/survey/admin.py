from django.contrib import admin

# Register your models here.
from .models import Client, Contact, Query, Item, ClientChange

for i in [Client, Contact, Query, Item, ClientChange]:
    admin.site.register(i)
