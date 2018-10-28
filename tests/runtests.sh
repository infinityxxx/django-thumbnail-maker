#!/bin/sh
export PYTHONPATH="./"
export DJANGO_SETTINGS_MODULE='settings'

export args="$@"
if [ -z "$args" ] ; then
    # avoid running the tests for django.contrib.* (they're in INSTALLED_APPS)
    export args="testapp thumbnail_maker"
fi

coverage run -a --branch --source=thumbnail_maker `which django-admin.py` test --traceback --settings=$DJANGO_SETTINGS_MODULE --verbosity 2 --pythonpath="../" $args
