# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v1
# Addon id: script.module.fuzzybritches_v1
# Addon Provider: The Papaw

import requests.sessions
from BeautifulSoup import BeautifulSoup

def get_source_info(url):
    source_info = {}
    if 'thevideo' in url:
        source_info['source'] = 'thevideo.me'
        with requests.session() as s:
            p = s.get(url)
            soup = BeautifulSoup(p.text, 'html.parser')
            title = soup.findAll('script', src=False, type=False)
            for i in title:
                if "title" in i.prettify():
                    for line in i.prettify().split('\n'):
                        if " title" in line:
                            line = line.replace("title: '", '').replace("',", '')
                            if "720" in line:
                                source_info['qual'] = "720p"
                            elif "1080" in line:
                                source_info['qual'] = "1080p"
                            else:
                                source_info['qual'] = "SD"
        return source_info
    elif 'vidzi' in url:
        #Not completed
        return "SD"