from PIL import Image
from django.db.models.fields.files import ImageFieldFile
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.fields import ImageField


class ImageWithThumbnailsFieldFile(ImageFieldFile):

    def save(self, name, content, save=True):
        super(ImageWithThumbnailsFieldFile, self).save(name, content, save)

        content.seek(0)
        image = Image.open(content)

        if image.mode not in ('L', 'RGB', 'RGBA'):
            image = image.convert('RGBA')

        make_thumbnails(image)

    def make_thumbnails(self, image):
        """
        Generate the thumbnails when file is uploaded
        """
        for thumb in self.field.thumbs:
            thumb_name, thumb_options = thumb
            geometry = thumb_options.pop('size')
            self.make_thumbnail(image, thumb_name, thumb_options, geometry)

    def make_thumbnail(self, image, thumb_name, thumb_options, geometry):
        """
        Generate separate thumbnail
        """
        get_thumbnail(image, geometry, thumb_options)


class ImageWithThumbnailsField(ImageField):

    attr_class = ImageWithThumbnailsFieldFile

    def __init__(self, *args, **kwargs):
        self.thumbs = kwargs.pop('thumbs', ())

        if not kwargs.has_key('max_length'):
            kwargs['max_length'] = 255

        super(ImageWithThumbnailsField, self).__init__(*args, **kwargs)
