#!/usr/bin/env python
#
# Parse OntoSoft's software listing
# and write in a CSV format
#
# Author: Karanjeet Singh
# Created on: April 13, 2017

import json
import argparse
import requests
import rdflib
import csv


class ParseListing(object):
    """
    Parse OntoSoft's software listing
    and write in a CSV format
    """

    def __init__(self, listing_url, output):
        self.listing_url = listing_url
        self.output = output
        self.csv_headers = ['"ID"', '"Name"', '"Description"', '"Location"']

    @staticmethod
    def fetch_content(url):
        header = {'x-requested-with': 'XMLHttpRequest'}
        response = requests.get(url, headers=header)
        return response.content

    def parse(self):
        listing_content = self.fetch_content(self.listing_url)
        listing = json.loads(listing_content)
        with open(self.output, 'wb') as out:
            out.write(','.join(self.csv_headers) + "\n")
            csvwriter = csv.writer(out, delimiter=',', quotechar='"')
            for software in listing:
                row = list()
                row.append(software['id'].encode('utf8'))
                row.append(software['label'].encode('utf8'))
                if software['description']:
                    row.append(software['description'].encode('utf8'))
                else:
                    row.append("")
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
                        row.append(obj.toPython().encode('utf8'))
                        break
                #print(row)
                csvwriter.writerow(row)


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-l', '--listing_url', help='Project Listing URL; Expects output in JSON format', required=True)
    argParser.add_argument('-o', '--output', help='Path to file where the output will be stored', required=True)
    args = argParser.parse_args()
    parser = ParseListing(args.listing_url, args.output)
    parser.parse()