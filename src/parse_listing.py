#!/usr/bin/env python
#
# Description
#
# Author: Karanjeet Singh
# Created on: April 13, 2017

import json
import argparse
import requests
import rdflib


class ParseListing(object):
    """
    Parse OntoSoft's software listing
    and write in a CSV format
    """

    def __init__(self, listing_url, output):
        self.listing_url = listing_url
        self.output = output
        self.csv_headers = ['"Name"', '"Description"', '"Location"']

    def fetch_content(self, url):
        header = {'x-requested-with': 'XMLHttpRequest'}
        response = requests.get(url, headers=header)
        return response.content

    def get_softwares(self):
        listing_content = self.fetch_content(self.listing_url)
        listing = json.loads(listing_content)
        with open(self.output, 'wb') as out:
            out.write(','.join(self.csv_headers) + "\n")
            for software in listing:
                row = ''
                row += '"' + software['label'] + '",'
                if software['description']:
                    row += '"' + software['description'] + '",'
                else:
                    row += '"",'
                details = self.fetch_content(software['id'])
                graph = rdflib.Graph()
                graph.parse(data=details, format="application/rdf+xml")
                loc_key = None
                for subject, predicate, obj in graph:
                    if 'hasCodeLocation' in predicate:
                        loc_key = obj
                        break
                if loc_key is None:
                    print("No location found for project: " + software['label'] + " with id: " + software['id'])
                    continue
                for subject, predicate, obj in graph:
                    if subject == loc_key and 'hasURI' in predicate:
                        row += '"' + obj.toPython() + '"'
                        break
                row += "\n"
                #print(row)
                out.write(row.encode('utf8'))


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-l', '--listing_url', help='Project Listing URL; Expects output in JSON format', required=True)
    argParser.add_argument('-o', '--output', help='Path to file where the output will be stored', required=True)
    args = argParser.parse_args()
    parser = ParseListing(args.listing_url, args.output)
    parser.get_softwares()