# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Real-Debrid Tools
# Addon id: plugin.video.rdtools
# Addon Provider: The Papaw

'''
Part of the PSMC Collection
'''

import json, re


def json_load_as_str(file_handle):
    return _byteify(json.load(file_handle, object_hook=_byteify), ignore_dicts=True)


def json_loads_as_str(json_text):
    return _byteify(json.loads(json_text, object_hook=_byteify), ignore_dicts=True)


def _byteify(data, ignore_dicts=False):
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    if isinstance(data, dict) and not ignore_dicts:
        return dict([(_byteify(key, ignore_dicts=True), _byteify(value, ignore_dicts=True)) for key, value in data.items()])
    return data

def title_key(title):
    try:
        if title is None: title = ''
        articles_en = ['the', 'a', 'an']
        articles_de = ['der', 'die', 'das']
        articles = articles_en + articles_de

        match = re.match('^((\w+)\s+)', title.lower())
        if match and match.group(2) in articles:
            offset = len(match.group(1))
        else:
            offset = 0

        return title[offset:]
    except:
        return title
