#!/usr/bin/python3

import configparser
import io
import MySQLdb
import os
import shutil
import subprocess
import sys

SCRIPT_LOCATION = os.path.dirname(os.path.realpath(__file__))
FILE_CONFIG = SCRIPT_LOCATION + '/../.env'
USER_FS_PATH = '/home/intercraftusers/%s/OpenComputers/%s'

def load_config():
    config = configparser.ConfigParser()
    try:
        with open(FILE_CONFIG) as f:
            ini_fp = io.StringIO('[root]\n' + f.read())
            config.readfp(ini_fp)
    except OSError:
        print('Please add and configure a database in config.json.')
        sys.exit(1)
    return config


def db_login(config):

    db = MySQLdb.connect(host=config['root']['DB_HOST'],
                         user=config['root']['DB_USERNAME'],
                         passwd=config['root']['DB_PASSWORD'],
                         db=config['root']['DB_DATABASE'])
    return db


def fetch_active_users(db):
    cur = db.cursor()
    query_string = 'SELECT `id`, `username` FROM `users` WHERE `active`=1 AND `username` IS NOT NULL'
    cur.execute(query_string)
    return cur.fetchall()


def fetch_filesystems(db, user_id):
    cur = db.cursor()
    query_string = 'SELECT `uuid` FROM `filesystems` WHERE `user_id`=%s'
    params = (user_id,)
    cur.execute(query_string, params)
    return [i[0] for i in cur.fetchall()]


def retrieve_mount_info():
    with open("/proc/mounts") as f:
        return f.read()


def mount_filesystems(config, username, filesystems):
    mount_info = retrieve_mount_info()
    mc_path = config['root']['MINECRAFT_SURVIVAL_ROOT']
    world_path = os.path.join(mc_path, config['root']['MINECRAFT_SURVIVAL_WORLD'])

    for uuid in filesystems:
        path = USER_FS_PATH % (username, uuid)
        fs_path = world_path + ('/opencomputers/%s' % uuid)
        if path in mount_info:
            print(uuid, 'is already mounted')
            continue
        if not os.path.exists(path):
            os.mkdir(path)
            shutil.chown(path, username, username)
        try:
            print('Mounting', uuid)
            params = ('mount', '--bind', fs_path, path)
            subprocess.run(params, timeout=5)
        except subprocess.TimeoutExpired:
            print("Failed to mount fs %s for user: %s" % (uuid, username))


def main():
    config = load_config()
    db = db_login(config)
    users = fetch_active_users(db)
    for user in users:
        filesystems = fetch_filesystems(db, user[0])
        mount_filesystems(config, user[1], filesystems)
    print("Successfully mounted filesystems!")


if __name__ == '__main__':
    main()
