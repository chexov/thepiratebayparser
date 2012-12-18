#!/usr/bin/env python
# encoding: utf-8

import thepiratebayparser.search
import piutils
import sys



show, season, episode = sys.argv[1].split(":")
OUT_DIR = sys.argv[2]

for qual in ('720p', 'HDTV'):
    q="%s S%sE%s %s" % (show, str(season).zfill(2), str(episode).zfill(2), qual)
    print q
    try:
        best = list(thepiratebayparser.search.search(q, '0/7/0'))[0]
        if int(best['seeders']) < 5:
            continue
    except thepiratebayparser.search.NoResults:
        print "no results"
        continue

    out = OUT_DIR + "{0}.magnet".format(unicode(best['title']))

    print "Best:", best['title'], best['seeders']
    print out

    piutils.fetch_magnet_url(best['url'], out)

    break

