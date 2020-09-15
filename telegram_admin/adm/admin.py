from django.contrib import admin

from .models import ShiftUser, Shift, Question, Result

admin.site.register(ShiftUser)
admin.site.register(Shift)
admin.site.register(Question)
admin.site.register(Result)
