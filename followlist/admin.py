from django.contrib import admin
from .models import SimpleUser, List, TypeList, Goal, Points

admin.site.register(SimpleUser)
admin.site.register(List)
admin.site.register(TypeList)
admin.site.register(Goal)
admin.site.register(Points)