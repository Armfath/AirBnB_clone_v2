#!/usr/bin/python3
""" Fabric to create an achieve for hbnb_web_static
"""


from fabric.api import *
import datetime

def do_pack():
    now = datetime.datetime.now()
    archive = './version/web_static_{}{}{}{}{}{}.tgz'.format(now.year,
        now.month, now.day, now.hour, now.minute, now.second)
    to_archive = './web_static'
    try:
        local('mkdir -p version && tar -czvf {} {}'.format(archive, to_archive))
        return (archive)
    except:
        return None
