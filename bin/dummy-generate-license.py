#!/usr/bin/env python

import sys
import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        description='Dummy license generator program.',
    )

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    parser.add_argument(
        'requestfile', nargs='?', help='input license request file')
    parser.add_argument(
        'licensefile', nargs='?', help='output license file')

    return parser


def parse_args(args=None, namespace=None, parser=None):
    if parser is None:
        parser = get_parser()

    args = parser.parse_args(args, namespace)

    return args


def generate_license_data(data):
    return data


def generte_license_file(istream, ostream):
    if istream in (None, '-'):
        istream = sys.stdin
    elif not hasattr(istream, 'read'):
        istream = open(istream, 'rb')

    if ostream in (None, '-'):
        ostream = sys.stdout
    elif not hasattr(ostream, 'write'):
        ostream = open(ostream, 'wb')

    request_data = istream.read()
    license_data = generate_license_data(request_data)
    ostream.write(license_data)


def main(args=None):
    args = parse_args(args)
    generte_license_file(args.requestfile, args.licensefile)


if __name__ == '__main__':
    main()
