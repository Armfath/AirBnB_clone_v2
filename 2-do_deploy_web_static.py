#!/usr/bin/python3
""" Fabric to deploy an achieve for hbnb_web_static and deploy to eb servers
"""
from fabric.api import local, env, put, run, settings
from datetime import datetime
import os


env.hosts = ['100.25.211.4',
             '100.26.234.235']
env.user = 'ubuntu'


def do_pack():
    """ Archive web_static
    """
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
    if os.path.exists(archive_path):
        archive_name_ext = archive_path.split('.')[-1]
        archive_name = archive_name_ext.split('.')[0]
    else:
        return False

    try:
        path = '/data/web_static/releases/{}'.format(archive_name)
        put('{}'.format(archive_path), '/tmp/')
        run('mkdir -p {}/'.format(path))
        run('tar -xzf /tmp/{} -C {}/'.format(archive_name_ext, path))
        run('rm /tmp/{}'.format(archive_name_ext))
        run('mv {}/web_static/* {}/'.format(path, path))
        run('rm -rf {}/web_static'.format(path))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(path))
        print("New version deployed!")
        return True
    except:
        return False
