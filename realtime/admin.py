from django.contrib import admin
from . import  models
# Register your models here.

@admin.register(models.TestModel)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name',)