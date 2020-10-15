# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches
# Addon id: script.module.fuzzybritches
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

import urllib, urlparse, re

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import trakt
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['gr']
        self.domains = ['xrysoi.se']
        self.base_link = 'http://xrysoi.se/'
        self.search_link = 'search/%s/feed/rss2/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'aliases': aliases,'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['title']
            year = data['year']
            query = '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)
            posts = client.parseDOM(r, 'item')

            for post in posts:
                try:
                    name = client.parseDOM(post, 'title')

                    links = client.parseDOM(post, 'a', ret='href')

                    t = re.sub('(\.|\(|\[|\s|)(\d{4})(\.|\)|\]|\s|)(.+|)', '',name[0])
                    if not cleantitle.get(t) == cleantitle.get(title): raise Exception()

                    y = re.findall('\(\s*(\d{4})\s*\)', name[0])[0]
                    if not y == year: raise Exception()

                    for url in links:
                        if any(x in url for x in ['.online', 'xrysoi.se', 'filmer', '.bp', '.blogger']): continue

                        url = client.replaceHTMLCodes(url)
                        url = url.encode('utf-8')
                        valid, host = source_utils.is_host_valid(url,hostDict)
                        if 'hdvid' in host: valid = True
                        if not valid: continue
                        quality = 'SD'
                        info = 'SUB'

                        sources.append({'source': host, 'quality': quality, 'language': 'gr', 'url': url, 'info': info, 'direct': False, 'debridonly': False})

                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url