from django.contrib import admin

# Register your models here.
from .models import Deposit, Kinri, Ois

admin.site.register(Deposit)
admin.site.register(Ois)
admin.site.register(Kinri)
