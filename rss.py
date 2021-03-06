#!/usr/bin/env python
# coding: utf-8
#
__author__ = 'Anton P. Linevich'
__title__ = 'thepiratebayparser.search'
__copyright__ = 'BSD Licence code. Enjoy and contribute'
__website__ = 'https://github.com/chexov/thepiratebayparser'

import sys
import time
import datetime

import feedparser
feedparser.USER_AGENT = "Mozilla/5.0"


def titles_by_url(url_or_xml, last_updated=None):
    """
    titles_by_url("http://rss.thepiratebay.org/user/d17c6a45441ce0bc0c057f19057f95e1")
    `last_updated` should be datetime.datetime object


    returns:
        [{'new': True,
          'title': u'The Ultimate Fighter S14E05 HDTV XviD-aAF [eztv]',
          'url': u'http://torrents.thepiratebay.org/6740475/The_Ultimate_Fighter_S14E05_HDTV_XviD-aAF_[eztv].6740475.TPB.torrent'},
         {'new': True,
          'title': u'Penn and Teller Tell a Lie S01E02 HDTV XviD-MOMENTUM [eztv]',
          'url': u'http://torrents.thepiratebay.org/6740436/Penn_and_Teller_Tell_a_Lie_S01E02_HDTV_XviD-MOMENTUM_[eztv].6740436.TPB.torrent'},
         {'new': True,
          'title': u'Blue Mountain State S03E05 Training Day HDTV XviD-FQM [eztv]',
          'url': u'http://torrents.thepiratebay.org/6740425/Blue_Mountain_State_S03E05_Training_Day_HDTV_XviD-FQM_[eztv].6740425.TPB.torrent'},
        ]
    """
    if not isinstance(last_updated, datetime.datetime):
        raise ValueError("last_updated value should be datetime.datetime object not {0}".format(type(last_updated)) )

    tries = 0
    while tries < 5:
        feed = feedparser.parse(url_or_xml, agent='Mozilla/5.0')
        print feed.get('updated')
        if not feed.get('updated'):
            print "Error getting RSS XML"
            print "Retyring..."
        else:
            print "OK"
            break
        tries = tries + 1
        time.sleep(tries+2)

    #feed_updated = datetime.datetime.fromtimestamp(time.mktime(feed.get('updated')))
    feed_updated = datetime.datetime.fromtimestamp(
        time.mktime(time.strptime(feed.get('updated'),"%a, %d %b %Y %H:%M:%S %Z"))
    ) #"Tue, 17 Jul 2012 13:35:03 GMT"

    for entry in feed.entries:
        title = entry.title

        # XXX: extracting x-bittorrent link. quickhack
        #r = filter(lambda i: i.type == u'application/x-bittorrent', entry.links)
        #torrent_url = None
        #if len(r) >= 1:
        #    torrent_url = r[0].href
        #else:
        #    raise ValueError(u"Can not find valid link %s" % entry.links)
        torrent_url = entry.links[0].href

        yield dict(title=title, url=torrent_url, last_updated=last_updated, new=(feed_updated > last_updated))


if __name__ == "__main__":
    # XXX: test function
    import pprint

    #url = 'http://rss.thepiratebay.org/user/d17c6a45441ce0bc0c057f19057f95e1'
    for url in sys.argv[1:]:
        pprint.pprint(list(titles_by_url(url, datetime.datetime.today())))

