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

import re,urlparse
from resources.lib.modules import cfscrape
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class s0urce:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['movie4k.is']
        self.base_link = 'https://www2.movie4k.is'
        self.search_link = '/search/%s/feed/rss2/'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search_id.replace(':', ' ').replace(' ', '+'))
            h = {'User-Agent': client.randomagent()}
            r = self.scraper.get(url, headers=h).content
            z = re.compile('<item>(.+?)</item>',flags=re.DOTALL | re.UNICODE | re.MULTILINE | re.IGNORECASE).findall(r)
            for t in z:
                b = re.compile('<a rel="nofollow" href="(.+?)">(.+?)</a>',flags=re.DOTALL | re.UNICODE | re.MULTILINE | re.IGNORECASE).findall(t)
                for foundURL, foundTITLE in b:
                    if cleantitle.get(title) in cleantitle.get(foundTITLE):
                        return foundURL
            return
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            h = {'User-Agent': client.randomagent()}
            html = self.scraper.get(url, headers=h).content
            qual = re.compile('<span class="calidad2">(.+?)</span>', flags=re.DOTALL | re.IGNORECASE).findall(html)[0]
            links = re.compile('<iframe src="(.+?)"', flags=re.DOTALL | re.UNICODE | re.MULTILINE | re.IGNORECASE).findall(html)
            for link in links:
                valid, host = source_utils.is_host_valid(link, hostDict)
                quality, info = source_utils.get_release_quality(qual, link)
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


