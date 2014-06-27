from django.db import models
from thumbnail_maker.fields import ImageWithThumbnailsField


class Item(models.Model):
    image = ImageWithThumbnailsField('image file', upload_to='upload',
                                     thumbs=('big', 'small'),)
