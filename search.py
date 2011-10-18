#!/usr/bin/env python
# encoding: utf-8
#
__author__ = 'Anton P. Linevich'
__title__ = 'thepiratebayparser.search'
__copyright__ = 'BSD Licence code. Enjoy and contribute'
__website__ = 'https://github.com/chexov/thepiratebayparser'

import lxml.html
import urllib
import urllib2
import sys


TPB_SEARCH_URL = "http://thepiratebay.org/search"


class HTMLDesignError(Exception):
    pass


def user(user, page=0):
    return search('user', "{user}/{page}/3".format(user=user, page=page), 'http://thepiratebay.org')


def search(q, category, search_url=TPB_SEARCH_URL):
    uri = urllib.quote("%s/%s" % (q, category))
    url = "%s/%s" % (search_url, uri)

    # Retriving HTML from the url
    print url
    html = urllib2.urlopen(url).read()

    root = lxml.html.fromstring(html)
    try:
        table = root.xpath('//table[@id="searchResult"]')
    except AssertionError:
        raise HTMLDesignError("The PirateBay site changed HTML desing. Please ping the author: {0}".format(url))

    if not table:
        raise ValueError("No search results")
    for el_tr in table[0].xpath('tr'):
        title = el_tr.xpath('td[2]/div[1]/a[1]/text()')

        if title:
            description = el_tr.xpath('td[2]/font[@class="detDesc"]/text()')[0]
            yield {
                   'title': title[0],
                   'url': el_tr.xpath('td[2]/a[1]/@href')[0],
                   'seeders': el_tr.xpath('td[3]/text()')[0],
                   'leachers': el_tr.xpath('td[4]/text()')[0],
                   'description': description,
                   'new': True,
                   }


if __name__ == "__main__":
    for row in search(sys.argv[1], '0/7/0'):
        print ("{se:>3} {le:>3} {desc} {url}".format(
            se=row['seeders'],
            le=row['leachers'],
            desc=row['description'],
            url=unicode(row['url']))
        )

