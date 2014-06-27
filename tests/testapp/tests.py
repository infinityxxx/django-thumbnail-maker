import os.path
import shutil

from django.conf import settings
from django.core import management
from django.test import TestCase

from .models import Item


DATA_DIR = os.path.join(settings.MEDIA_ROOT, 'data')


class BaseTestCase(TestCase):

    def setUp(self):
        try:
            os.makedirs(settings.MEDIA_ROOT)
        except OSError, e:
            if e.errno != 17:
                raise

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)


class ModelTestCase(BaseTestCase):
    def setUp(self):
        super(ModelTestCase, self).setUp()


class TemplateTestCase(BaseTestCase):
    pass


class CommandTestCase(BaseTestCase):
    def setUp(self):
        super(CommandTestCase, self).setUp()
        Item.objects.get_or_create(image='data/bamboo.png')
        Item.objects.get_or_create(image='data/flower.png')

    def test_make_thumbnail(self):
        management.call_command('make_thumbnails', 'testapp.Item', 'image', verbosity=1)
