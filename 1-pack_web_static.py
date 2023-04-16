#!/usr/bin/python3
""" Fabric to create an achieve for hbnb_web_static
"""
from fabric.api import *
from datetime import datetime


def do_pack():
    """ Archive web_static
    """
    now = datetime.now()
    archive = './versions/web_static_{}{}{}{}{}{}.tgz\
    '.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    to_archive = './web_static'
    create_archive = local('mkdir -p versions && tar -czvf {} {}'
                           .format(archive, to_archive))
    if (create_archive.return_code == 0):
        return (archive)
    else:
        return None
