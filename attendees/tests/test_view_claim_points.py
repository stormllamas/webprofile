from django.test import TestCase
from django.urls import reverse, resolve
from ..views import claim_points
from ..forms import PointsForm

class AttendeesClaimPointsViewTest(TestCase):
    def setUp(self):
        url = reverse('attendees:claim_points')
        self.response = self.client.get(url)

    def test_payments_url_resolves_payments_view(self):
        view = resolve('/qr/claim_points/')
        self.assertEqual(view.func, claim_points)

    def test_navbar_breadcrumb_links_exists(self):
        index_url = reverse('attendees:index')
        self.assertContains(self.response,'href="{0}"'.format(index_url))

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PointsForm)

    def test_points_invalid_post_data_empty_fields(self):
        url = reverse('attendees:claim_points')
        data = {
            'amount': ''
        }
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)