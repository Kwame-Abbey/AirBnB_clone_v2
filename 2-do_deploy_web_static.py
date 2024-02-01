#!/usr/bin/python3
"""generates a .tgz file from the contens of web_static using FABRIC"""
from fabric.api import *
import datetime
import os.path
import re


env.hosts = ['54.158.211.83', '54.90.1.20']


@runs_once
def do_pack():
    """ generarates .tgz archive from web_static folder """
    local("mkdir -p versions")
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    r = local("tar -cvzf versions/web_static_{}.tgz ./web_static".
              format(now), capture=True)
    if r.succeeded:
        return ("versions/web_static_{}.tgz".format(now))
    else:
        return


def do_deploy(archive_path):
    """ distributes an archive to web servers """
    if not os.path.isfile(archive_path):
        return False
    upload = put(archive_path, "/tmp", use_sudo=True)
    path = re.compile("versions\/(.+)\.tgz")
    file_name = path.search(archive_path).group(1)
    create_folder = run("sudo mkdir -p /data/web_static/releases/{}/".
                        format(file_name))
    unzip = run("sudo tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/".
                format(file_name, file_name))
    remove_archive = run("sudo rm /tmp/{}.tgz".format(file_name))
    string1 = "sudo mv /data/web_static/releases/{}/web_static/*"
    string2 = "/data/web_static/releases/{}/"
    string = string1 + " " + string2
    move_files = run(string.format(file_name, file_name))
    rm_webstatic = run("sudo rm -rf /data/web_static/releases/{}/web_static".
                       format(file_name))
    rm_link = run("sudo rm -rf /data/web_static/current")
    s = "sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
    create_l = run(s.format(file_name))
    if upload.succeeded and create_folder.succeeded\
        and create_folder.succeeded and unzip.succeeded\
            and remove_archive.succeeded and move_files.succeeded\
            and rm_webstatic.succeeded and rm_link.succeeded\
            and create_l.succeeded:
        return True
    return False
