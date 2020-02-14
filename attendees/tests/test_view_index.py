from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone
import datetime

from django.contrib.auth.models import User

from ..models import Attendee
from ..views import index
from ..forms import PointsForm, CSVForm

from PIL import Image
from django.utils.six import BytesIO


def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)
    
def create_attendee(first_name, last_name, days):
    """
    Create a attendee with the given `first_name and last_name` and timestamp is the
    given number of `days` offset to now (negative for attendees timestamped
    in the past, positive for attendees that have yet to be timestamped).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Attendee.objects.create(first_name=first_name, last_name=last_name, timestamp=time)

class AttendeesIndexViewTest(TestCase):
    def setUp(self):
        url = reverse('attendees:index')
        self.response = self.client.get(url)

    def test_index_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_index_url_resolves_index_view(self):
        view = resolve('/qr/')
        self.assertEqual(view.func, index)

    def test_has_attendees(self):
        create_attendee(first_name='John', last_name='Doe', days=0)
        attendee_detail_url = reverse('attendees:details', kwargs={'pk':1})
        response = self.client.get(reverse('attendees:index'))
        self.assertTrue(Attendee.objects.exists())
        self.assertContains(response, 'Doe, John')
        self.assertContains(response, 'Absent')
        self.assertContains(response, 'href="{0}"'.format(attendee_detail_url))

    def test_no_attendees(self):
        self.assertContains(self.response, 'No Attendees Registered')
        self.assertQuerysetEqual(self.response.context['attendees'], [])
        
    def test_functions_links_exists(self):
        qrscanner_url = reverse('attendees:qrscanner')
        qrgenerated_url = reverse('attendees:qrgenerated')
        redeem_points_url = reverse('attendees:redeem_points')
        claim_points_url = reverse('attendees:claim_points')
        admin_url = '/admin'
        self.assertContains(self.response, 'href="{0}"'.format(qrscanner_url))
        self.assertContains(self.response, 'href="{0}"'.format(qrgenerated_url))
        self.assertContains(self.response, 'href="{0}"'.format(redeem_points_url))
        self.assertContains(self.response, 'href="{0}"'.format(claim_points_url))
        self.assertContains(self.response, 'href="{0}"'.format(admin_url))

    def test_navbar_links_exists(self):
        index_url = reverse('index')
        attendees_index_url = reverse('attendees:index')
        activity_url = reverse('attendees:activity')
        attendee_upload_url = reverse('attendees:attendee_upload')
        self.assertContains(self.response, 'href="{0}"'.format(index_url))
        self.assertContains(self.response, 'href="{0}"'.format(attendees_index_url))
        self.assertContains(self.response, 'href="{0}"'.format(activity_url))
        self.assertContains(self.response, 'href="{0}"'.format(attendee_upload_url))

    def test_navbar_links_exists_not_authenticated_user(self):
        signup_url = reverse('signup')
        login_url = reverse('login')
        self.assertContains(self.response, 'href="{0}"'.format(signup_url))
        self.assertContains(self.response, 'href="{0}"'.format(login_url))

    def test_navbar_links_exists_authenticated_user(self):
        user = User.objects.create_user(username='susiesalmon', password='abc123', email='ss@gmail.com', first_name='Susie', last_name='Salmon')
        self.client.login(username='susiesalmon', password='abc123')
        my_account_url = reverse('my_account')
        logout_url = reverse('logout')
        url = reverse('attendees:index')
        response = self.client.get(url)
        self.assertTrue(User.objects.exists())
        self.assertTrue(user.is_authenticated)
        self.assertContains(response, 'href="{0}"'.format(my_account_url))
        self.assertContains(response, 'href="{0}"'.format(logout_url))

    