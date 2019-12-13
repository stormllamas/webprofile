from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'message', 'contact_date')
    list_display_links = ('name',)
    list_filter = ('contact_date',)
    list_per_page = 25
    search_fields = ('subject', 'message')

admin.site.register(Contact, ContactAdmin)