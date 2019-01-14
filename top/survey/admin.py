from django.contrib import admin

# Register your models here.
from .models import Block, Client, Person, Query, Item, ClientChange, Vendor, QueryChange

for i in [Client, Person, Query, Item, ClientChange, Block, Vendor, QueryChange]:
    admin.site.register(i)
