#!/usr/bin/env python
# encoding: utf-8

import lxml.html
import urllib
import urllib2
import sys

class HTMLDesignError(Exception): pass

TPB_SEARCH_URL="http://thepiratebay.org/search"

def search(q, category):
    uri = urllib.quote("%s/%s" % (q, category))
    url = "%s/%s" % (TPB_SEARCH_URL, uri)
    # Retriving the HTML from url
    html = urllib2.urlopen(url).read()

    root = lxml.html.fromstring(html)
    try:
        table = root.xpath('//table[@id="searchResult"]')
    except AssertionError:
        raise HTMLDesignError(u"The PirateBay site changed HTML desing. Please ping the author: %s" %(url))

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

