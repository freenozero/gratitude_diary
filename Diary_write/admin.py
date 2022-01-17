from django.contrib import admin
from Diary_write.models import data
# Register your models here.

class datainfo(admin.ModelAdmin):
    list_display = ('id', 'email', 'content', 'date')

admin.site.register(data, datainfo)