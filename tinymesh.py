#!/usr/bin/env python3
import os
import sys
from tinymesh_http import resources, auth
import argparse
from pprint import pprint


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


apiauth = None
if args.token:
    apiauth = auth.TokenV1Auth(args.token)
elif args.auth:
    username, password = args.auth.split(":")
    apiauth = apiauth.BasicAuth(username, password)
elif 'TM_API_TOKEN' in os.environ:
    token = bytes(os.environ['TM_API_TOKEN'], 'utf-8')
    apiauth = auth.TokenV1Auth(token)
else:
    try:
        with open(os.path.expanduser("~/.tinymesh/token"), 'rb') as fd:
            token = fd.read()
            # lazy, ignorant way of removing newlines from token
            if 10 == token[len(token)-1]:
                token = token[:len(token)-1]

            apiauth = auth.TokenV1Auth(token)
    except:
        pass


if 'list' == args.command[0]:
    if 1 == len(args.command):
        parser.print_usage()
        print("No resource type specified")
        sys.exit(1)
    elif 'network' == args.command[1]:
        pprint(resources.Network.list(apiauth))
    elif 'organization' == args.command[1]:
        pprint(resources.Organization.list(apiauth))
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
        pprint(resources.Network.read(args.command[2], apiauth))
    elif 'organization' == args.command[1]:
        pprint(resources.Network.read(args.command[1], apiauth))
    else:
        parser.print_usage()
        print("Can't read unknown resource", args.command[1])
        sys.exit(1)
else:
    parser.print_usage()
