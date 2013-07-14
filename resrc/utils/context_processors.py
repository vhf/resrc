# -*- coding: utf-8 -*-:
import sys
import django


def versions(request):
    return {
        'django_version': '{0}.{1}.{2}'.format(
            django.VERSION[0], django.VERSION[1], django.VERSION[2]),
        'python_version': '{0}.{1}.{2}'.format(
            sys.version_info[0], sys.version_info[1], sys.version_info[2])
    }
