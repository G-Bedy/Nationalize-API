from django.contrib import admin

from .models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count', 'country')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('count',)
    ordering = ('id',)


admin.site.register(Person, PersonAdmin)
