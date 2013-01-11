#!/usr/bin/env python3
# encoding: utf-8
#
__author__ = 'Anton P. Linevich'
__title__ = 'thepiratebayparser.search'
__copyright__ = 'BSD Licence code. Enjoy and contribute'
__website__ = 'https://github.com/chexov/thepiratebayparser'

import urllib
import urllib.request
import sys

import lxml.html
import lxml.etree


TPB_SEARCH_URL = "http://thepiratebay.se/search"


class HTMLDesignError(Exception):
    pass


class NoResults(Exception):
    pass


def user(user, page=0):
    return search('user', "{user}/{page}/3".format(user=user, page=page), 'http://thepiratebay.se')


def search(q, category, search_url=TPB_SEARCH_URL):
    uri = urllib.request.quote("%s/%s" % (q, category))
    url = "%s/%s" % (search_url, uri)

    print ("Retrieving HTML from the url", url)
    html = urllib.request.urlopen(url).read()

    root = lxml.html.fromstring(html.decode())
    try:
        table = root.xpath('//table[@id="searchResult"]')
    except AssertionError:
        raise HTMLDesignError("The PirateBay site changed HTML layout. Please ping the module author with this url: {0}".format(url))

    if not table:
        raise NoResults(html)
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
        print ("{se:>3} {le:>3} {desc} %{url}s".format(
            se=row['seeders'],
            le=row['leachers'],
            desc=row['description'],
            url=(row['url'])
        ))

