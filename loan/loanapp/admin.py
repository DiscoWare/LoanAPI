from django.contrib import admin
from .models import Header
from .models import *

admin.site.register(Header)
admin.site.register(Application)
admin.site.register(ApplicationBusiness)