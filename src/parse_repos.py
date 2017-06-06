#!/usr/bin/env python
#
# Parse repository URLs from extracted
# software listing
#
# Author: Karanjeet Singh
# Created on: April 16, 2017


import csv
import argparse
import sys
import os


class ParseRepos(object):
    def __init__(self, parsed_listing, output):
        self.parsed_listing = parsed_listing
        self.output = output

    @staticmethod
    def parse_github_repo(loc):
        return '/'.join(loc.split('/')[0:5])

    def parse(self, typ):
        repos = set()
        with open(self.parsed_listing, 'rb') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            with open(os.path.join(self.output,'list.csv'), 'wb') as out:
                out_writer = csv.writer(out, delimiter=',', quotechar='"')
                try:
                    next(reader, None) # Skipping header
                    for row in reader:
                        if typ in row[3]:
                            out_writer.writerow(row)
                            if typ == 'github':
                                repos.add(self.parse_github_repo(row[3]))
                                print(row)
                except csv.Error, e:
                    sys.exit('Error reading file %s, line %d: %s' % (self.parsed_listing, reader.line_num, e))

        with open(os.path.join(self.output, 'repo.txt'), 'wb') as out:
            for repo in repos:
                out.write(repo + "\n")


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-p', '--parsed_listing', help='Path to input generated from parse_listing.py',
                           required=True)
    argParser.add_argument('-o', '--output', help='Output directory path; Should exist', required=True)
    argParser.add_argument('-t', '--type', help='Repository Type; Eg: github', required=True)
    args = argParser.parse_args()
    parser = ParseRepos(args.parsed_listing, args.output)
    parser.parse(args.type)