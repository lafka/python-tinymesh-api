#!/usr/bin/env python3
import os, sys
from tinymesh import resources, auth
import argparse
from pprint import pprint


token = b"koUl1ZoL7L/0+hrinsrBpjpOaizDC5CqQgkAUtm4DMpgEIo11tn0LHRL5gSUtbfJCy5N5424OMqU/NEA/SSzFw=="
fingerprint = "f98baed49376af73c741ece9c8fd48acfae69efdd6d097beba10abc79da1c076"

token = None

parser = argparse.ArgumentParser(description="Tiny Mesh Cloud Client",
                                 add_help=True)

parser.add_argument('--token', '-t', default=None, help="""
    Token to use, if neither --token or --auth is given the program will check
    the environment for TM_AUTH_TOKEN and last the file ~/.tinymesh/token for a
    suitable token.
    """)

parser.add_argument('--auth', '-a', default=None, help="""
    User/password pair, separated by `:`. Ie --auth dev@example:password
    """)

parser.add_argument('command', help="""
    Operation and optional resource selector and/or body
    """, metavar='command', nargs='+', default=None)

args = parser.parse_args()


if args.token:
    token = args.token
elif args.auth:
    pass
elif 'TM_API_TOKEN' in os.environ:
    token = bytes(os.environ['TM_API_TOKEN'], 'utf-8')
else:
    try:
        with open(os.path.expanduser("~/.tinymesh/token"), 'rb') as fd:
            token = fd.read()
            # lazy, ignorant way of removing newlines from token
            if 10 == token[len(token)-1]:
                token = token[:len(token)-1]
    except:
        pass

auth = auth.TokenV1Auth(token)


if 'list' == args.command[0]:
    if 1 == len(args.command):
        parser.print_usage()
        print("No resource type specified")
        sys.exit(1)
    elif 'network' == args.command[1]:
        pprint(resources.Network.list(auth))
    elif 'organization' == args.command[1]:
        pprint(resources.Organization.list(auth))
    else:
        parser.print_usage()
        print("Can't list unknown resource", args.command[1])
        sys.exit(1)

elif 'read' == args.command[0]:
    if 1 == len(args.command):
        parser.print_usage()
        print("No resource type specified")
        sys.exit(1)
    if 'network' == args.command[1]:
        pprint(resources.Network.read(args.command[2], auth))
    elif 'organization' == args.command[1]:
        pprint(resources.Network.read(args.command[1], auth))
    else:
        parser.print_usage()
        print("Can't read unknown resource", args.command[1])
        sys.exit(1)
else:
    parser.print_usage()

#if
#
#networks = resources.Organization.list(auth)
#
