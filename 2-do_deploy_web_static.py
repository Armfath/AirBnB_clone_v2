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


def do_deploy(archive_path):
    """ Distributes an archive to your web servers
    """
    import os
    if os.path.exists(archive_path):
        archive_name_e = os.path.basename(archive_path)
        archive_name = archive_name_e.split('.')[0]
    else:
        return False

    root = '/data/web_static'
    try:
        put('{}'.format(archive_path), '/tmp/{}'.format(archive_name_e))
    except:
        return False

    print("New version deployed!")
    return True
