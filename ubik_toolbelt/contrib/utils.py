# coding: utf-8
import os
import pwd
import grp

def user_exists(user):
    try:
        pwd.getpwnam(user)
        return True
    except KeyError:
        return False

def group_exists(group):
    try:
        grp.getgrnam(group)
        return True
    except KeyError:
        return False

def get_user_name():
    return pwd.getpwuid(os.getuid()).pw_name

def get_user_group():
    return grp.getgrgid(pwd.getpwuid(os.getuid()).pw_gid).gr_name