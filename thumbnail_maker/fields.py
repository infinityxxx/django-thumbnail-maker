from PIL import Image
from django.db.models.fields.files import ImageFieldFile
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.fields import ImageField


class ImageWithThumbnailsFieldFile(ImageFieldFile):

    def save(self, name, content, save=True):
        super(ImageWithThumbnailsFieldFile, self).save(name, content, save)
        self.make_thumbnails(self.name)

    def make_thumbnails(self, file_name):
        """
        Generate the thumbnails when file is uploaded
        """
        for thumb_name, (geometry, thumb_options) in self.field.thumbs.iteritems():
            self.make_thumbnail(file_name, thumb_name, thumb_options, geometry)

    def make_thumbnail(self, file_name, thumb_name, thumb_options, geometry):
        """
        Generate separate thumbnail
        """
        get_thumbnail(file_name, geometry, **thumb_options)


class ImageWithThumbnailsField(ImageField):

    attr_class = ImageWithThumbnailsFieldFile

    def __init__(self, *args, **kwargs):
        self.thumbs = kwargs.pop('thumbs', {})

        if not kwargs.has_key('max_length'):
            kwargs['max_length'] = 255

        super(ImageWithThumbnailsField, self).__init__(*args, **kwargs)
