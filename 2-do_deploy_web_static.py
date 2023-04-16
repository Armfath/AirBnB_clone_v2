#!/usr/bin/python3
""" Fabric to deploy an achieve for hbnb_web_static and deploy to eb servers
"""
from fabric.api import local, env, put, run, settings


env.hosts = ['100.25.211.4',
             '100.26.234.235']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """ Archive web_static
    """
    import datetime
    now = datetime.datetime.now()
    archive = './versions/web_static_{}{}{}{}{}{}.tgz\
    '.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    to_archive = './web_static'
    create_archive = local('mkdir -p versions && tar -czvf {} {}'
                           .format(archive, to_archive))
    if (create_archive.return_code == 0):
        return (archive)
    else:
        return None
