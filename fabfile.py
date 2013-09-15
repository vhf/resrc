from fabric.api import local

TEST_APPS = ('link', 'list', 'page', 'tag', 'userprofile', 'utils')


def test(integration=1):
    command = './manage.py test -v 2 --settings=resrc.test_settings'
    command += " --exclude='feeback'"
    if int(integration) == 0:
        command += " --exclude='integration_tests'"
    local(command)


try:
    from fabfile_local import *
except ImportError:
    pass
