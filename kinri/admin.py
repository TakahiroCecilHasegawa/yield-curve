from django.contrib import admin

# Register your models here.
#from .models import KinriConfig
from .models import Deposit, Future, Kinri, Ois

admin.site.register(Deposit)
admin.site.register(Future)
admin.site.register(Ois)
admin.site.register(Kinri)
