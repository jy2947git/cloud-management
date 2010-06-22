#!/usr/bin/python
#
#    Query and display EC2 metadata related to the AMI instance
#    Copyright (c) 2009 Canonical Ltd. (Canonical Contributor Agreement 2.5)
#
#    Author: Alon Swartz <alon@turnkeylinux.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Query and display EC2 metadata

If no options are provided, all options will be displayed

Options:
    -h --help               show this help

    --kernel-id             display the kernel id
    --ramdisk-id            display the ramdisk id
    --reservation-id        display the reservation id

    --ami-id                display the ami id
    --ami-launch-index      display the ami launch index
    --ami-manifest-path     display the ami manifest path
    --ancestor-ami-id       display the ami ancestor id
    --product-codes         display the ami associated product codes
    --availability-zone     display the ami placement zone

    --instance-id           display the instance id
    --instance-type         display the instance type

    --local-hostname        display the local hostname
    --public-hostname       display the public hostname

    --local-ipv4            display the local ipv4 ip address
    --public-ipv4           display the public ipv4 ip address

    --block-device-mapping  display the block device id
    --security-groups       display the security groups

    --public-keys           display the openssh public keys
    --user-data             display the user data (not actually metadata)

"""

import sys
import time
import getopt
import urllib
import socket
import traceback
METAOPTS = ['ami-id', 'ami-launch-index', 'ami-manifest-path',
            'ancestor-ami-id', 'availability-zone', 'block-device-mapping',
            'instance-id', 'instance-type', 'local-hostname', 'local-ipv4',
            'kernel-id', 'product-codes', 'public-hostname', 'public-ipv4',
            'public-keys', 'ramdisk-id', 'reserveration-id', 'security-groups',
            'user-data']

class Error(Exception):
    pass

class EC2Metadata:
    """Class for querying metadata from EC2"""

    def __init__(self, addr='169.254.169.254', api='2008-02-01'):
        self.addr = addr
        self.api = api

        if not self._test_connectivity(self.addr, 80):
            raise Error("could not establish connection to: %s" % self.addr)

    @staticmethod
    def _test_connectivity(addr, port):
        for i in range(6):
            s = socket.socket()
            
            try:
                print("trying to connect " + addr + ":" + str(port) + " try " + str(i))
                s.settimeout(2)
                s.connect((addr, port))
                s.close()
                return True
            except socket.error, e:
                print("error:",sys.exc_info()[0])
                traceback.print_exc()
                time.sleep(1)

        return False

    def _get(self, uri):
        url = 'http://%s/%s/%s/' % (self.addr, self.api, uri)
        value = urllib.urlopen(url).read()
        if "404 - Not Found" in value:
            return None

        return value

    def get(self, metaopt):
        """return value of metaopt"""

        if metaopt not in METAOPTS:
            raise Error('unknown metaopt', metaopt, METAOPTS)

        if metaopt == 'availability-zone':
            return self._get('meta-data/placement/availability-zone')

        if metaopt == 'public-keys':
            data = self._get('meta-data/public-keys')
            keyids = [ line.split('=')[0] for line in data.splitlines() ]

            public_keys = []
            for keyid in keyids:
                uri = 'meta-data/public-keys/%d/openssh-key' % int(keyid)
                public_keys.append(self._get(uri).rstrip())

            return public_keys

        if metaopt == 'user-data':
            return self._get('user-data')

        return self._get('meta-data/' + metaopt)

def get(metaopt):
    """primitive: return value of metaopt"""

    m = EC2Metadata()
    return m.get(metaopt)

def display(metaopts, prefix=False):
    """primitive: display metaopts (list) values with optional prefix"""

    m = EC2Metadata()
    for metaopt in metaopts:
        value = m.get(metaopt)
        if not value:
            value = "unavailable"

        if prefix:
            print "%s: %s" % (metaopt, value)
        else:
            print value

def usage(s=None):
    """display usage and exit"""

    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    """handle cli options"""

    try:
        getopt_metaopts = METAOPTS[:]
        getopt_metaopts.append('help')
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", getopt_metaopts)
    except getopt.GetoptError, e:
        usage(e)

    if len(opts) == 0:
        display(METAOPTS, prefix=True)
        return

    metaopts = []
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()

        metaopts.append(opt.replace('--', ''))

    display(metaopts)


if __name__ == "__main__":
   main()
