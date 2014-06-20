import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    args = "<app.model> <field>"
    help = "Auto generate thumbnails for all instances of " \
           "the given model, for the given field."

    def handle(self, *args, **options):
        self.args = args
        self.options = options

        self.validate_input()
        self.parse_input()
        self.make_thumbnails()

    def validate_input(self):
        num_args = len(self.args)

        if num_args < 2:
            raise CommandError("Please pass the app.model and the field.")
        if num_args > 2:
            raise CommandError("Too many arguments.")

        if '.' not in self.args[0]:
            raise CommandError("The first argument must be: app.model")

    def parse_input(self):
        """
        Get input parameters
        """
        app, model_name = self.args[0].split('.')
        model_name = model_name.lower()

        try:
            self.model = ContentType.objects.get(app_label=app, model=model_name)
            self.model = self.model.model_class()
        except ContentType.DoesNotExist:
            raise CommandError("There is no app/model: %s" % self.args[0])

        self.field = self.args[1]

    def make_thumbnails(self):
        """
        Auto-generating the thumbnails for given model's field
        """
        Model = self.model
        for instance in Model.objects.all():
            field = getattr(instance, self.field)
            field.make_thumbnails(field.name)
            print "Thumbnail for pk=%s: %s" % (instance.pk, field.name)
