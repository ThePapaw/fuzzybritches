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

import json
import urllib, urlparse, re

from resources.lib.modules import client
from resources.lib.modules import source_utils


class s0urce:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdbest.net', 'ffull.net']
        self.base_link = 'https://vikv.net/'
        self.embed_link = 'https://api.hdv.fun/embed/{}'
        self.frames_link = 'https://api.hdv.fun/'
        self.sub_link = 'https://sub1.hdv.fun/vtt1/{}.vtt'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except :
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            imdb = data['imdb']
            url = self.embed_link.format(imdb)
            data = client.request(url, referer=self.base_link)
            frames_link = re.findall('''\$\.post\('(.+?)',{'imdb''', data, re.DOTALL)[0]
            frames_link = urlparse.urljoin(self.frames_link, frames_link) if frames_link.startswith('/') else frames_link
            try:
                get_ip = client.request('https://whatismyipaddress.com')
                ip = re.findall('''/ip/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})['"]''', get_ip, re.DOTALL)[0]
            except IndexError:
                ip = '0'
            post = {'imdb': imdb, 'ip': ip}
            frames = client.request(frames_link, post=post)
            frames = json.loads(frames)
            for url in frames:
                try:
                    subs = url['sub']
                    sub = re.findall('''sub_id['"]:\s*(\d+)\,.+?lg['"]:\s*u['"]greek['"]''', str(subs))[0]
                except :
                    subs = url['sub']
                    sub = re.findall('''sub_id['"]:\s*(\d+)\,.+?lg['"]:\s*u['"]english['"]''', str(subs))[0]

                sub = self.sub_link.format(sub)
                link = url['src'][0]['src']
                quality = url['src'][0]['label']

                url = link.replace(' ', '%20') + '|User-Agent={}&Referer={}'.format(
                    urllib.quote(client.agent()), 'https://redirector.googlevideo.com/')
                quality, info = source_utils.get_release_quality(quality)

                sources.append(
                    {'source': 'GVIDEO', 'quality': quality, 'language': 'en', 'url': url, 'sub': sub,
                     'direct': True, 'debridonly': False})

            return sources
        except :
            return sources

    def resolve(self, url):
        return url