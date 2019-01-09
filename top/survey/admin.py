from django.contrib import admin

# Register your models here.
from .models import Block, Client, Person, Query, Item, ClientChange, PersonChange, Vendor, Certificate, PriceCat

for i in [Client, Person, Query, Item, ClientChange, PersonChange, Block, Vendor, Certificate, PriceCat]:
    admin.site.register(i)
