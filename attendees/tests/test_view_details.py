from django.test import TestCase
from ..models import Attendee, ActivityLog
from ..views import AttendeeActivities
from django.urls import reverse, resolve
from django.utils import timezone
import datetime


def create_attendee(first_name, last_name, days):
    """
    Create a attendee with the given `first_name and last_name` and timestamp is the
    given number of `days` offset to now (negative for attendees timestamped
    in the past, positive for attendees that have yet to be timestamped).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Attendee.objects.create(first_name=first_name, last_name=last_name, timestamp=time)

def create_activity(attendee):
    """
    Create an activity with an attendee
    """
    return ActivityLog.objects.create(attendee=attendee)

class AttendeesDetailsViewTest(TestCase):
    def setUp(self):
        create_attendee(first_name='John', last_name='Doe', days=0)
        url = reverse('attendees:details', kwargs={'pk':1})
        self.response = self.client.get(url)

    def test_details_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_details_view_not_found_status_code(self):
        url = reverse('attendees:details', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_details_url_resolves_detail_view(self):
        view = resolve('/qr/details/1')
        self.assertEqual(view.func.view_class, AttendeeActivities)

    def test_navbar_breadcrumb_links_exists(self):
        index_url = reverse('attendees:index')
        self.assertContains(self.response, 'href="{0}"'.format(index_url))

    def test_function_links_exists(self):
        edit_attendee_url = reverse('attendees:edit_attendee', kwargs={'pk':1})
        self.assertContains(self.response, 'href="{0}"'.format(edit_attendee_url))

    def test_activity_exists(self):
        url = reverse('attendees:details', kwargs={'pk':1})
        attendee = Attendee.objects.get(pk=1)
        create_activity(attendee)
        response = self.client.get(url)
        self.assertTrue(ActivityLog.objects.exists())
        self.assertContains(response, 'John Doe', 4)
        self.assertContains(response, '0.00', 3)

    def test_no_activity_exists(self):
        self.assertFalse(ActivityLog.objects.exists())
        self.assertContains(self.response, 'No activity yet')
        
    