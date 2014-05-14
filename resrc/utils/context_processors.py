# -*- coding: utf-8 -*-:

def version(request):
    """Returns the current deployed version."""

    try:
        from subprocess import check_output
        git_version = check_output(['git', 'rev-parse', 'HEAD'])
    except:
        git_version = 'unknown'

    return {
        'version': "{0}-{1}".format("1.0.0", git_version[:6])
    }
