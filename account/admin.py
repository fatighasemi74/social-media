from django.contrib import admin
from . models import UserAccount, Relation, Data

# Register your models here.
admin.site.register(Data)
admin.site.register(UserAccount)
admin.site.register(Relation)
