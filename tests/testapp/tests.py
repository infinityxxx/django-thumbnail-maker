import os.path
import shutil

from django.conf import settings
from django.core import management
from django.template.loader import render_to_string
from django.test import TestCase

from .models import Item


DATA_DIR = os.path.join(settings.MEDIA_ROOT, 'data')


class BaseTestCase(TestCase):

    def setUp(self):
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
            shutil.copytree(settings.DATA_ROOT, DATA_DIR)

    def tearDown(self):
        pass
        shutil.rmtree(settings.MEDIA_ROOT)


class ModelTestCase(BaseTestCase):
    def setUp(self):
        super(ModelTestCase, self).setUp()


class TemplateTestCase(BaseTestCase):
    def setUp(self):
        super(TemplateTestCase, self).setUp()
        self.item, created = Item.objects.get_or_create(image='data/bamboo.png')

    def test_templatetag(self):

        val = render_to_string('usethumbnail_big.html', {
            'item': self.item,
        }).strip()
        self.assertEqual(val, '<img width="500" height="400">')

        val = render_to_string('usethumbnail_small.html', {
            'item': self.item,
        }).strip()
        self.assertEqual(val, '<img width="80" height="80">')


class CommandTestCase(BaseTestCase):
    def setUp(self):
        super(CommandTestCase, self).setUp()
        Item.objects.get_or_create(image='data/bamboo.png')
        Item.objects.get_or_create(image='data/flower.png')

    def test_make_thumbnail(self):
        management.call_command('make_thumbnails', 'testapp.Item', 'image', verbosity=1)
