#!/usr/bin/env python
# encoding: utf-8

import lxml.html
import sys

TPB_SEARCH_URL="http://thepiratebay.org/search"

def search(q, category):
    url = "%s/%s/%s" % (TPB_SEARCH_URL, q, category)
    tree = lxml.html.parse(url)
    table = tree.xpath('//table[@id="searchResult"]')
    if not table:
        raise ValueError(u"No search results")
    for el_tr in table[0].xpath('tr'):
        description = unicode(el_tr.xpath('td[2]/font[@class="detDesc"]/text()')[0]).encode('utf-8')
        yield {'torrent': el_tr.xpath('td[2]/a[1]/@href')[0],
               'seeders': el_tr.xpath('td[3]/text()')[0],
               'leachers': el_tr.xpath('td[4]/text()')[0],
               'description': unicode(el_tr.xpath('td[2]/font[@class="detDesc"]/text()')[0]).encode('utf-8'),
               }


if __name__ == "__main__":
    for row in search(sys.argv[1], '0/7/0'):
        print ("{se:>3} {le:>3} {desc} {url}".format(
            se=row['seeders'],
            le=row['leachers'],
            desc=row['description'],
            url=unicode(row['torrent'])) )

