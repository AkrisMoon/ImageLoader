from django.test import TestCase
from django.urls import reverse

from ImageLoader.models import Image
from ImageLoader.forms import ImageCreateForm, ImageResizeForm

class ImageTestCase(TestCase):
    def setUp(self):
        Image.objects.create(url = 'http://placehold.it/100x86', width= 100, height= 100)

    def test_create_object_without_image(self):
        form = ImageCreateForm(data = {'image': None, 'url': None})
        self.assertFalse(form.is_valid())

    def test_get_absolute_url(self):
        image = Image.objects.get(id=1)
        self.assertEqual(image.get_absolute_url(), '/resize/1/')

    def test_resize_image(self):
        image1 = Image.objects.create(pk = 2, url = 'http://placehold.it/100x86', height=100)
        response = self.client.post(
            reverse('resize_image', kwargs={'pk': image1.id}),
            {'height': 50})
        self.assertEqual(response.status_code, 302)
        image2 = Image.objects.get(pk = 3)
        self.assertEqual(image2.height, 50)
        self.assertEqual(image1.height, 100)
