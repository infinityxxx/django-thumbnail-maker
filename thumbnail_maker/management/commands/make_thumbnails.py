"""
Additional commands for thumbnails
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType

from optparse import make_option


class Command(BaseCommand):
    args = "<app.model> <field>"
    option_list = BaseCommand.option_list + (
        make_option('--force', '-f', action='store_true',
                    dest='force', default=False,
                    help='Force update of thumbnails'),
    )
    help = "Auto-generate thumbnails for all instances of " \
           "the given model for the given field."

    def handle(self, *args, **options):
        self.args = args
        self.force = options.get('force')
        self.validate_input()
        self.parse_input()
        self.make_thumbnails(force=self.force)

    def validate_input(self):
        num_args = len(self.args)

        if num_args < 2:
            raise CommandError("Please pass `app.model` and `field`")
        if num_args > 2:
            raise CommandError("Too many arguments")

        if '.' not in self.args[0]:
            raise CommandError("The first argument must be: app.model")

    def parse_input(self):
        """
        Get input parameters
        """
        app, model_name = self.args[0].split('.')
        model_name = model_name.lower()

        try:
            self.model = ContentType.objects.get(
                app_label=app, model=model_name
            )
            self.model = self.model.model_class()
        except ContentType.DoesNotExist:
            raise CommandError("Not found app/model: %s" % self.args[0])

        self.field = self.args[1]

    def make_thumbnails(self, force=False):
        """
        Auto-generating the thumbnails for given model's field
        """
        Model = self.model
        for instance in Model.objects.all():
            field = getattr(instance, self.field)
            field.make_thumbnails(field.name, force=force)
            print "Thumbnail for pk=%s: %s" % (instance.pk, field.name)
