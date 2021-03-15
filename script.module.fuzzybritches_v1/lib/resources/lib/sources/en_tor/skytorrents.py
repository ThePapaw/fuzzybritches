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

import re, urllib, urlparse
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import debrid
from resources.lib.modules import source_utils


class s0urce:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.skytorrents.lol']
        self.base_link = 'https://www.skytorrents.net'
        self.search_link = '/?search=%s'
        self.min_seeders = int(control.setting('torrent.min.seeders'))

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url == None: return sources
            if debrid.status() == False: raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode']))if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            try:
                posts = client.parseDOM(r, 'tbody', attrs={'id': 'results'})
                for post in posts:
                    link = re.findall('a href="(magnet:.+?)" title="(.+?)"', post, re.DOTALL)
                    for url, data in link:
                        if not hdlr in data: continue
                        url = url.split('&tr')[0]
                        url = url.encode('ascii', 'ignore')
                        quality, info = source_utils.get_release_quality(data)
                        if any(x in url for x in ['FRENCH', 'Ita', 'italian', 'TRUEFRENCH', '-lat-','Dublado']): continue
                        info = ' | '.join(info)
                        sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
            except:
                return
            return sources
        except :
            return sources

    def resolve(self, url):
        return url
