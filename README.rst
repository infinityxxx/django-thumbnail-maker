
Auto-generator of thumbnails for Django, using sorl-thumbnail.

Features
========

- Auto-genarates thumbnails using sorl-thumbnail while uploading (saving) images
- You can use any engines & plugins you usually use with sorl-thumbnail
- The application does not replace thumbnail templatetag and you can use everything you want from sorl-thumbnail
- Command for auto-generating of missing thumbnails

How to Use
==========

Get the code
------------

Get the code for the latest stable release use pip::

   $ pip install django-thumbnail-maker

Install in your project
-----------------------

Register 'thumbnail_maker', in the 'INSTALLED_APPS' section of
your project's settings::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.admin',
        'django.contrib.sites',
        'django.contrib.comments',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.contenttypes',

        'thumbnail_maker',
    )


Set up your model's field
-------------------------

Use 'ImageWithThumbnailsField' and 'thumbs' option as a dictionary to set up all required.
First parameter in a dictionary is a geometry string(used in sorl-thumbnail),
second is a dictionary with options (crop, quality, padding, format, etc.)::

    from django.db import models
    from thumbnail_maker import ImageWithThumbnailsField

    class Item(models.Model):
        image = ImageWithThumbnailsField(
            upload_to='somewhere',
            thumbs={
                'langing_page': ('400x300', {'crop': 'center',
                                             'quality': 90}),
                '50x50':        ('50x50',   {}),
                'any_name':     ('5x277',   {'padding': True})
            }
        )


Templates Usage
---------------

All of the examples assume that you first load the thumbnail_maker template tag in
your template::

    {% load thumbnail_maker %}


A simple usage. ::

    {% usethumbnail item.image "landing_page" as im %}
        <img src="{{ im.url }}" width="{{ im.width }}" height="{{ im.height }}">
    {% endusethumbnail %}

    {% usethumbnail item.image "50x50" as im %}
        <img src="{{ im.url }}" width="{{ im.width }}" height="{{ im.height }}">
    {% endusethumbnail %}

