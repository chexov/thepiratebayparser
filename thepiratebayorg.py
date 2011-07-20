#!/usr/bin/env python
# encoding: utf-8

import lxml.html
import sys

TPB_SEARCH_URL="http://thepiratebay.org/search"

class NoResultsException(Exception):
    pass


def search(q, category):
    url = "%s/%s/%s" % (TPB_SEARCH_URL, q, category)
    tree = lxml.html.parse(url)
    table = tree.xpath('//table[@id="searchResult"]')
    if not table:
        raise NoResultsException(u"No search results")
    for el_tr in table[0].xpath('tr'):
        yield {'torrent': el_tr.xpath('td[2]/a[1]/@href')[0],
               'seeders': el_tr.xpath('td[3]/text()')[0],
               'leachers': el_tr.xpath('td[4]/text()')[0],
               }


if __name__ == "__main__":
    for row in search(sys.argv[1], '0/7/0'):
        print u"%-3s %-3s %s" % (row['seeders'], row['leachers'],
                row['torrent'])

