#!/usr/bin/python3
"""Distributes an archive to the web servers
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['54.158.211.83', '54.90.1.20']
env.user = "ubuntu"


def do_pack():
    """ Generates a tgz archive from the contents of
    the web_static folder of the AirBnB clone
    """
    try:
        my_time = datetime.now().strftime('%Y%m%d%H%M%S')
        local("mkdir -p versions")
        my_file = 'versions/web_static_' + my_time + '.tgz'
        local('tar -vzcf {} web_static'.format(my_file))
        return (my_file)
    except Exception:
        return None


def do_deploy(archive_path):
    """distributes an archive to my web servers
    """
    path_existence = os.path.exists(archive_path)
    if path_existence is False:
        return False
    try:
        path_split = archive_path.replace('/', ' ').replace('.', ' ').split()
        just_directory = path_split[0]
        no_tgz_name = path_split[1]
        full_filename = path_split[1] + '.' + path_split[2]
        folder = '/data/web_static/releases/{}/'.format(no_tgz_name)
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(folder))
        run('tar -xzf /tmp/{} -C {}/'.format(full_filename, folder))
        run('rm /tmp/{}'.format(full_filename))
        run('mv {}/web_static/* {}'.format(folder, folder))
        run('rm -rf {}/web_static'.format(folder))
        current = '/data/web_static/current'
        run('rm -rf {}'.format(current))
        run('ln -s {}/ {}'.format(folder, current))
        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
