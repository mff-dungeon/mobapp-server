from django.contrib import admin
from .models import *

# Register your models here.
models = (
    Bundle, ContactInfo, ContactUser, Ticket
)

for m in models:
    admin.site.register(m)
