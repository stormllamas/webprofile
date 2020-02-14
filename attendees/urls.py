from django.urls import path
from . import views

app_name = 'attendees'
urlpatterns = [
    path('', views.index, name='index'),
    path('overview/', views.overview, name='overview'),
    path('qrgenerated/', views.qrgenerated, name='qrgenerated'),
    path('qrscanner/', views.qrscanner, name='qrscanner'),
    path('details/<int:pk>', views.AttendeeActivities.as_view(), name = 'details'),
    path('activity_log/', views.Activity.as_view(), name = 'activity'),
    path('upload-csv/', views.attendee_upload, name= 'attendee_upload'),
    path('edit_attendee/<int:pk>', views.AttendeeUpdateView.as_view(), name='edit_attendee'),
    path('claim_points/', views.claim_points, name='claim_points'),
    path('redeem_points/', views.redeem_points, name='redeem_points'),
    path('confirmation/<int:attendee_id>', views.confirmation, name='confirmation'),
]