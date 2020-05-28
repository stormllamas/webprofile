from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import Contact, SiteConfiguration

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'message', 'contact_date')
    list_display_links = ('name',)
    list_filter = ('contact_date',)
    list_per_page = 25
    search_fields = ('subject', 'message')

admin.site.register(Contact, ContactAdmin)

admin.site.register(SiteConfiguration, SingletonModelAdmin)
# config = SiteConfiguration.get_solo()
config = SiteConfiguration.objects.get()