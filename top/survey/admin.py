from django.contrib import admin

# Register your models here.
from .models import Block, Client, Person, Query, Item, ClientChange, PersonChange, Vendor, Certificate, PriceCat, QueryChange

for i in [Client, Person, Query, Item, ClientChange, PersonChange, Block, Vendor, Certificate, PriceCat, QueryChange]:
    admin.site.register(i)
