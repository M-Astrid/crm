from django.contrib import admin

# Register your models here.
from .models import Block, Client, Person, Query, Item, ClientChange, PersonChange

for i in [Client, Person, Query, Item, ClientChange, PersonChange, Block]:
    admin.site.register(i)
