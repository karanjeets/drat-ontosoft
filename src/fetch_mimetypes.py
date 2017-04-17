#!/usr/bin/env python
#
# Retrieves all mime types from
# DRAT Solr statistics core
#
# Author: Karanjeet Singh
# Created on: April 16, 2017

import pysolr
import argparse


class FetchMimeTypes(object):
    def __init__(self, solr_url, rows, is_count):
        self.solr_server = pysolr.Solr(solr_url)
        self.rows = rows
        self.is_count = is_count

    @staticmethod
    def parse_mime(v):
        return v.split('_', 1)[1]

    def fetch(self):
        mime = {}
        response = self.solr_server.search('*:*', None, fl='mime_*', rows=self.rows)
        print('Number of rows selected: ' + str(len(response.docs)))
        for doc in response.docs:
            for key in doc:
                m = self.parse_mime(key)
                if m not in mime:
                    mime[m] = 0
                mime[m] += 1
        if self.is_count:
            print(mime)
        else:
            out = ''
            for key in mime.keys():
                out += '"' + key + '",'
            print(out[0:-1])


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--solr_url', help='DRAT Solr URL', required=True)
    argparser.add_argument('-d', '--docs', help='Maximum documents to query from Solr', required=True)
    argparser.add_argument('-c', '--count', action='store_true', default=False,
                           help='Add this if you need count of each mime type', required=False)
    args = argparser.parse_args()
    fetcher = FetchMimeTypes(args.solr_url, args.docs, args.count)
    fetcher.fetch()