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
        archive_name_ext = os.path.basename(archive_path)
        archive_name = archive_name_ext.split('.')[0]
    else:
        return False

    path = '/data/web_static/releases/{}'.format(archive_name)
    with settings(warn_only=True):
        opp_1 = put('{}'.format(archive_path), '/tmp/')
        opp_2 = run('mkdir -p {}/'.format(path))
        opp_3 = run('tar -xzf /tmp/{} -C {}/'.format(archive_name_ext, path))
        opp_4 = run('rm /tmp/{}'.format(archive_name_ext))
        opp_5 = run('mv {}/web_static/* {}/'.format(path, path))
        opp_6 = run('rm -rf {}/web_static'.format(path))
        opp_7 = run('rm -rf /data/web_static/current')
        opp_8 = run('ln -s {}/ /data/web_static/current'.format(path))

        if (opp_1.failed or
                opp_2.failed or
                opp_3.failed or
                opp_4.failed or
                opp_5.failed or
                opp_6.failed or
                opp_7.failed or
                opp_8.failed):
            return False

    print("New version deployed!")
    return True
