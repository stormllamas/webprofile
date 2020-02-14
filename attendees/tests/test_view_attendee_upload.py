from django.test import TestCase
from django.urls import reverse, resolve

from PIL import Image
from django.utils.six import BytesIO
from django.core.files import File

from ..views import attendee_upload
from ..forms import CSVForm

# def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
#     """
#     Generate a test image, returning the filename that it was saved as.

#     If ``storage`` is ``None``, the BytesIO containing the image data
#     will be passed instead.
#     """
#     data = BytesIO()
#     Image.new(image_mode, size).save(data, image_format)
#     data.seek(0)
#     if not storage:
#         return data
#     image_file = ContentFile(data.read())
#     return storage.save(filename, image_file)

def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)

class AttendeesUploadViewTest(TestCase):
    def setUp(self):
        url = reverse('attendees:attendee_upload')
        self.response = self.client.get(url)

    def test_attendee_upload_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_upload_url_resolves_payments_view(self):
        view = resolve('/qr/upload-csv/')
        self.assertEqual(view.func, attendee_upload)

    def test_navbar_breadcrumb_links_exists(self):
        index_url = reverse('attendees:index')
        self.assertContains(self.response,'href="{0}"'.format(index_url))
        
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CSVForm)

    def test_payments_valid_post_data(self):
        url = reverse('attendees:attendee_upload')
        avatar = create_image(None, 'avatar.csv')
        data = {
            'file': avatar
        }
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertFalse(form.errors)

    def test_payments_invalid_post_data(self):
        url = reverse('attendees:attendee_upload')
        # avatar = create_image(None, 'avatar.png')
        avatar = get_image_file()
        data = {
            'file': avatar
        }
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'That was not a CSV file')

    def test_payments_invalid_post_data_empty_fields(self):
        url = reverse('attendees:attendee_upload')
        data = {
            'file': ''
        }
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)