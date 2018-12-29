from django.contrib import admin

# Register your models here.
from .models import Block, Client, Person, Query, Item, ClientChange

for i in [Client, Person, Query, Item, ClientChange, Block]:
    admin.site.register(i)
