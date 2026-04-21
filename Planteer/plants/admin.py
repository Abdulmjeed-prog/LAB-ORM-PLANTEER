from django.contrib import admin
from .models import Plant, Comment, Country
# Register your models here.

class PlantAdmin(admin.ModelAdmin):

    list_display = ('name','used_for')
    list_filter = ('category',)

admin.site.register(Plant,PlantAdmin)
admin.site.register(Comment)
admin.site.register(Country)