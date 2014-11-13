#!/usr/bin/env python
# conf/nagios.py
# -*- coding: utf-8 -*-

# Config parameters for project library
# path         : Used by www/lib/host.py
#                - nagioscfg - path of nagios main config file

import os

base = {
    "cfg_dir" : "/usr/local/nagios/etc/nagweb",
}

path = {
    "baseDir" : os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "nagioscfg" : "/usr/local/nagios/etc/nagios.cfg",
    "hostcfg" : "{}/nagweb_hostcfg.cfg".format(base["cfg_dir"]),
    "hostgroupcfg" : "{}/nagweb_hostgroupcfg.cfg".format(base["cfg_dir"]),
}
