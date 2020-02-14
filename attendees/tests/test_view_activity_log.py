from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone
import datetime

from ..models import Attendee, ActivityLog
from ..views import Activity

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

class AttendeesIndexViewTest(TestCase):
    def setUp(self):
        url = reverse('attendees:activity')
        self.response = self.client.get(url)

    def test_index_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_index_url_resolves_index_view(self):
        view = resolve('/qr/activity_log')
        self.assertEqual(view.func.view_class, Activity)

    def test_has_activity(self):
        create_attendee(first_name='John', last_name='Doe', days=0)
        attendee = Attendee.objects.get(pk=1)
        create_activity(attendee)
        response = self.client.get(reverse('attendees:activity'))
        self.assertTrue(ActivityLog.objects.exists())
        self.assertTrue(Attendee.objects.exists())
        self.assertContains(response, 'John Doe')
        self.assertContains(response, '0.00', 3)