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
    with settings(warn_only=True):
        opp_1 = put(f'{archive_path}', f'/tmp/{archive_name_e}')
        opp_2 = run(f'mkdir -p {root}/releases/{archive_name}/')
        opp_3 = run(f'tar -xzf /tmp/{archive_name_e}\
                    -C {root}/releases/{archive_name}/')
        opp_4 = run(f'rm /tmp/{archive_name_e}')
        opp_5 = run(f'mv {root}/releases/{archive_name}/web_static/*\
                    {root}/releases/{archive_name}/')
        opp_6 = run(f'rm -rf {root}/releases/{archive_name}/web_static')
        opp_7 = run(f'rm -rf {root}/current')
        opp_8 = run(f'ln -s {root}/releases/{archive_name}/ {root}/current')

        if (opp_1.failed or
                opp_2.failed or
                opp_3.failed or
                opp_4.failed or
                opp_5.failed or
                opp_6.failed or
                opp_7.failed or
                opp_8.failed):
            return False
