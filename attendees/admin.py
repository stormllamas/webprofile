from django.contrib import admin
from .models import Attendee, ActivityLog, Designation

# def ActivityLog(self, request, id):
#     return ActivityLog.as_view()(request.id)
    
class ActivityLogInLine(admin.TabularInline):
    model = ActivityLog
    extra = 1
    verbose_name = "Activity".lower()
    verbose_name_plural = "Activity".lower()

class AttendeeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['last_name', 'first_name', 'designation', 'email', 'contact', 'membership']}),
        ('Time Information',  {'fields': ['present', 'timestamp']}),
        ('Card Value',        {'fields': ['points_earned', 'points_redeemed', 'points_balance']}),
    ]
    inlines = [ActivityLogInLine]
    list_display = ('last_name', 'first_name', 'present', 'points_earned', 'points_redeemed', 'points_balance', 'timestamp')
    list_editable = ('present', 'points_earned', 'points_redeemed', 'points_balance')
    list_filter = ['present', 'timestamp']

admin.site.register(Attendee, AttendeeAdmin)

class ActivityLogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['attendee', 'time_log', 'points_claim', 'points_redeem', 'total-points-earned', 'total_points_redeemed', 'total_points_balance']})
    ]

# admin.site.register(ActivityLog, ActivityLogAdmin)
class AttendeeInLine(admin.TabularInline):
    model = Attendee
    extra = 1

class DesignationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                {'fields': ['name']}),
    ]
    inlines = [AttendeeInLine]
    list_display = ('name',)

admin.site.register(Designation, DesignationAdmin)