# Copyright (c) 2014 Cisco Systems
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
"""
Used to get the APIC and MySQL login credentials from the command
line (--help gives usage).

The login credentials are taken in the following order:
* Command line arguments
* Environment variables
* File named credentials.py
* From an interactive prompt

These are done in a per credential basis so it is possible to specify only
some of the arguments.  For instance, the username and URL can be specified
in credentials.py but the password can be taken from the user through the
interactive prompt.  Another example is using the command line argument to
override the URL specified in credentials.py to temporarily connect to a
different APIC.
"""
import argparse
import os
import sys
import getpass


class Credentials(object):
    def __init__(self, qualifier='apic', description=''):
        def set_default(key):
            if 'APIC_' + key.upper() in os.environ.keys():
                return os.environ['APIC_' + key.upper()]
            else:
                try:
                    import credentials
                except ImportError:
                    return None
                try:
                    default = credentials.__getattribute__(key.upper())
                    return default
                except AttributeError:
                    return None

        if isinstance(qualifier, str):
            qualifier = (qualifier)
        self._qualifier = qualifier
        self._parser = argparse.ArgumentParser(description=description)
        if 'apic' in qualifier:
            DEFAULT_URL = set_default('url')
            DEFAULT_LOGIN = set_default('login')
            DEFAULT_PASSWORD = set_default('password')
            self._parser.add_argument('-u', '--url',
                                      default=DEFAULT_URL,
                                      help='APIC IP address.')
            self._parser.add_argument('-l', '--login',
                                      default=DEFAULT_LOGIN,
                                      help='APIC login ID.')
            self._parser.add_argument('-p', '--password',
                                      default=DEFAULT_PASSWORD,
                                      help='APIC login password.')
        if 'mysql' in qualifier:
            DEFAULT_MYSQL_IP = set_default('mysqlip')
            DEFAULT_MYSQL_LOGIN = set_default('mysqllogin')
            DEFAULT_MYSQL_PASSWORD = set_default('mysqlpassword')
            self._parser.add_argument('-i', '--mysqlip',
                                      default=DEFAULT_MYSQL_IP,
                                      help='MySQL IP address.')
            self._parser.add_argument('-a', '--mysqllogin',
                                      default=DEFAULT_MYSQL_LOGIN,
                                      help='MySQL login ID.')
            self._parser.add_argument('-s', '--mysqlpassword',
                                      default=DEFAULT_MYSQL_PASSWORD,
                                      help='MySQL login password.')

    def get(self):
        self._args = self._parser.parse_args()
        self.verify()
        return self._args

    def add_argument(self, *args, **kwargs):
        self._parser.add_argument(*args, **kwargs)

    def verify(self):
        if 'apic' in self._qualifier:
            if self._args.login is None:
                try:
                    self._args.login = raw_input('APIC login username: ')
                except NameError:
                    self._args.login = input('APIC login username: ')
            if self._args.url is None:
                try:
                    self._args.url = raw_input('APIC URL: ')
                except NameError:
                    self._args.url = input('APIC URL: ')
            if self._args.password is None:
                self._args.password = getpass.getpass('APIC Password: ')
        if 'mysql' in self._qualifier:
            if self._args.mysqlip is None:
                try:
                    self._args.mysqlip = raw_input('MySQL IP address: ')
                except NameError:
                    self._args.mysqlip = input('MySQL IP address: ')
            if self._args.mysqllogin is None:
                try:
                    self._args.mysqllogin = raw_input('MySQL login username: ')
                except NameError:
                    self._args.mysqllogin = input('MySQL login username: ')
            if self._args.mysqlpassword is None:
                self._args.mysqlpassword = getpass.getpass('MySQL Password: ')
