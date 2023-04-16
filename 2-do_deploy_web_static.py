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
        put(f'{archive_path}', f'/tmp/{archive_name_e}')
        run(f'mkdir -p {root}/releases/{archive_name}/')
        run(f'tar -xzf /tmp/{archive_name_e}\
                -C {root}/releases/{archive_name}/')
        run(f'rm /tmp/{archive_name_e}')
        run(f'mv {root}/releases/{archive_name}/web_static/*\
                {root}/releases/{archive_name}/')
        run(f'rm -rf {root}/releases/{archive_name}/web_static')
        run(f'rm -rf {root}/current')
        run(f'ln -s {root}/releases/{archive_name}/ {root}/current')
    except:
        return False

    print("New version deployed!")
    return True
