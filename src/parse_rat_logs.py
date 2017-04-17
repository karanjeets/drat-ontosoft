#!/usr/bin/env python
#
# Retrieves all mime types from
# DRAT Solr statistics core
#
# Author: Karanjeet Singh
# Created on: April 16, 2017

import argparse
import glob


class ParseRat(object):
    def __init__(self, input):
        self.input = input

    @staticmethod
    def parse_license(s):
        li_dict = {'N': 'Notes', 'B': 'Binaries', 'A': 'Archives', 'AL': 'Apache', '!?????': 'Unknown'}
        arr = s.split("/", 1)
        li = arr[0].strip()
        if arr[0].strip() not in li_dict:
            print('LICENSE TYPE NOT FOUND. PLEASE ADD.')
        else:
            li = li_dict[li]
        return ['/' + arr[1].strip(), li]

    def parse(self):
        rat_license = {}
        rat_header = {}
        for filename in glob.glob(self.input):
            print('=' * 20)
            section = 0
            l = 0
            h = 0
            cur_file = ''
            cur_header = ''
            with open(filename, 'rb') as f:
                for line in f:
                    if '*****************************************************' in line:
                        section += 1
                    if section == 4:
                        l += 1
                        if l > 5:
                            line = line.strip()
                            if line:
                                li = self.parse_license(line)
                                rat_license[li[0]] = li[1]
                                #print(li)
                    if section == 5:
                        if '=====================================================' in line or '== File:' in line:
                            h += 1
                        if h == 2:
                            cur_file = '/' + line.split("/", 1)[1].strip()
                        if h == 3:
                            cur_header += line
                        if h == 4:
                            rat_header[cur_file] = cur_header.split("\n", 1)[1]
                            cur_file = ''
                            cur_header = ''
                            h = 1
            if h == 3:
                rat_header[cur_file] = cur_header.split("\n", 1)[1]

        for key in rat_header:
            print('Key: ' + key + ', License: ' + rat_license[key] + ', Header: ' + rat_header[key])


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-in', '--input', help='Directory containing RAT logs; Compatible with RegEx', required=True)
    args = argparser.parse_args()
    parser = ParseRat(args.input)
    parser.parse()
