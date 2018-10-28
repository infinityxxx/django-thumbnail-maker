import os.path
import shutil

from django.conf import settings
from django.core import management
from django.core.files import File
from django.template import TemplateSyntaxError
from django.template.loader import render_to_string
from django.test import TestCase

from testapp.models import Item


DATA_DIR = os.path.join(settings.MEDIA_ROOT, 'data')


class BaseTestCase(TestCase):

    def setUp(self):
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
            shutil.copytree(settings.DATA_ROOT, DATA_DIR)

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)


class ModelTestCase(BaseTestCase):
    def test_auto_generating_thumbs(self):
        self.item = Item()
        self.item.image.save(
            'bamboo.png',
            File(open(os.path.join(settings.DATA_ROOT, 'bamboo.png'), 'rb')),
            save=False
        )
        # small: 80x80
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    settings.MEDIA_ROOT,
                    #'cache/65/04/650496dff97f883e3df125025a2dcd65.jpg'
                    'cache/3a/83/3a8334660aa38c27220ef11e8681ea06.jpg'

                )
            )
        )

        # big: 500x400
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    settings.MEDIA_ROOT,
                    #'cache/72/58/7258f6b747cba3161d7866fbb66ccd87.jpg'
                    'cache/4a/20/4a2010bd55d5605a75cad0338f38f72e.jpg'

                )
            )
        )


class TemplateTestCase(BaseTestCase):
    def setUp(self):
        super(TemplateTestCase, self).setUp()
        self.item, created = Item.objects.get_or_create(
            image='data/bamboo.png'
        )

    def test_templatetag(self):

        val = render_to_string('testapp/usethumbnail_big.html', {
            'item': self.item,
        }).strip()
        self.assertEqual(val, '<img width="500" height="400">')

        val = render_to_string('testapp/usethumbnail_small.html', {
            'item': self.item,
        }).strip()
        self.assertEqual(val, '<img width="80" height="80">')

        with self.assertRaises(TemplateSyntaxError):
            val = render_to_string('testapp/usethumbnail_error.html', {
                'item': self.item,
            }).strip()


class CommandTestCase(BaseTestCase):
    def setUp(self):
        super(CommandTestCase, self).setUp()
        Item.objects.get_or_create(image='data/bamboo.png')
        Item.objects.get_or_create(image='data/flower.jpg')

    def test_make_thumbnail(self):
        management.call_command('make_thumbnails', 'testapp.Item', 'image', verbosity=1)

        for f in ('cache/65/04/650496dff97f883e3df125025a2dcd65.jpg',
                  'cache/72/58/7258f6b747cba3161d7866fbb66ccd87.jpg',
                  'cache/84/8f/848f13e3183c0ed9bb5d96eb95de70f0.jpg',
                  'cache/ed/87/ed875125009a8755bc64944268e81557.jpg'):
            self.assertTrue(
                os.path.exists(os.path.join(settings.MEDIA_ROOT, f))
            )

    def test_make_thumbnail_force(self):
        management.call_command('make_thumbnails', 'testapp.Item', 'image', verbosity=1, force=True)

        for f in ('cache/65/04/650496dff97f883e3df125025a2dcd65.jpg',
                  'cache/72/58/7258f6b747cba3161d7866fbb66ccd87.jpg',
                  'cache/84/8f/848f13e3183c0ed9bb5d96eb95de70f0.jpg',
                  'cache/ed/87/ed875125009a8755bc64944268e81557.jpg'):
            self.assertTrue(
                os.path.exists(os.path.join(settings.MEDIA_ROOT, f))
            )

    def test_make_thumbnail_error(self):
        with self.assertRaises(management.CommandError):
            management.call_command('make_thumbnails', 'testapp.Item', verbosity=1)

        with self.assertRaises(management.CommandError):
            management.call_command('make_thumbnails', 'testapp.Item', 'image', 'arg', verbosity=1)

        with self.assertRaises(management.CommandError):
            management.call_command('make_thumbnails', 'Item', 'image', verbosity=1)

        with self.assertRaises(management.CommandError):
            management.call_command('make_thumbnails', 'noapp.Noitem', 'image', verbosity=1)
