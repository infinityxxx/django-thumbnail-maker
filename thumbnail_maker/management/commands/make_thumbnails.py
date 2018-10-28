"""
Additional commands for thumbnails
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Auto-generate thumbnails for all instances of " \
           "the given model for the given field."

    def add_arguments(self, parser):
        """Required and optional arguments."""
        # required arguments:
        parser.add_argument('app_model', type=str)
        parser.add_argument('field', type=str)

        # optional arguments:
        parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Force update of thumbnails',
        )

    def handle(self, *args, **options):
        self.args = args
        self.force = options.get('force')
        self.model = self.get_model(options['app_model'])
        self.field = options['field']
        self.make_thumbnails(force=self.force)

    def get_model(self, app_model):
        """Parse `app_model` string and return model class."""
        try:
            app, model_name = app_model.split('.')
        except ValueError:
            raise CommandError("The first argument must be: app.model")

        model_name = model_name.lower()

        try:
            model = ContentType.objects.get(
                app_label=app, model=model_name
            )
            model = model.model_class()
        except ContentType.DoesNotExist:
            raise CommandError("Not found app/model: {}".format(app_model))
        else:
            return model

    def make_thumbnails(self, force=False):
        """
        Auto-generating the thumbnails for given model's field
        """
        Model = self.model
        for instance in Model.objects.all():
            field = getattr(instance, self.field)
            field.make_thumbnails(field.name, force=force)
            print("Thumbnail for pk=%s: %s" % (instance.pk, field.name))
