"""
Required model fields
"""
from django.db.models.fields.files import ImageFieldFile
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.default import (kvstore as sorl_kvstore,
                                    storage as sorl_storage,
                                    backend as sorl_backend)
from sorl.thumbnail.fields import ImageField
from sorl.thumbnail.images import ImageFile

from thumbnail_maker.helpers import get_thumbnail_options


class ImageWithThumbnailsFieldFile(ImageFieldFile):
    """
    ImageFieldFile from sorl-thumbnail saving thumbnails on upload,
    using field.thumbs option
    """
    def save(self, name, content, save=True):
        """
        Generate pre-defined thumbnails on field save
        """
        super(ImageWithThumbnailsFieldFile, self).save(
            name, content, save
        )
        self.make_thumbnails(self.name)

    def make_thumbnails(self, file_name, force=False):
        """
        Generate the thumbnails when file is uploaded
        """
        for thumbname, (geometry, options) in self.field.thumbs.items():
            self.make_thumbnail(file_name, thumbname, options,
                                geometry, force=force)

    def make_thumbnail(self, file_name, thumb_name, thumb_options,
                       geometry, force=False):
        """
        Generate separate thumbnail.
        Generate new thumbnail if `force` is True.
        """
        if force:
            source = ImageFile(file_name, sorl_storage)
            full_options = get_thumbnail_options(source, thumb_options)
            thumb_name = sorl_backend._get_thumbnail_filename(
                source, geometry, full_options
            )
            thumb = ImageFile(thumb_name, sorl_storage)
            sorl_kvstore._delete(thumb.key)
        get_thumbnail(file_name, geometry, **thumb_options)


class ImageWithThumbnailsField(ImageField):
    """
    ImageField from sorl-thumbnail saving `thumbs` option
    """
    attr_class = ImageWithThumbnailsFieldFile

    def __init__(self, *args, **kwargs):
        """
        Pre-define thumbs that will be auto-generated on save.
        """
        self.thumbs = kwargs.pop('thumbs', {})
        super(ImageWithThumbnailsField, self).__init__(*args, **kwargs)
