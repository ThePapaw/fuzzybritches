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

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

import json,os,xbmc,xbmcaddon,xbmcvfs

from resources.lib.modules import control

addonInfo = xbmcaddon.Addon().getAddonInfo
dataPath = xbmcvfs.translatePath(addonInfo('profile'))
favouritesFile = os.path.join(dataPath, 'favourites.db')
progressFile = os.path.join(dataPath, 'progress.db')
def getFavourites(content):
    try:
        dbcon = database.connect(favouritesFile)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT * FROM %s" % content)
        items = dbcur.fetchall()
        items = [(i[0], eval(i[1])) for i in items]
    except:
        items = []

    return items


def getProgress(content):
    try:
        dbcon = database.connect(progressFile)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT * FROM %s" % content)
        items = dbcur.fetchall()
        items = [(i[0], eval(i[1])) for i in items]
    except:
        items = []

    return items


def addFavourite(meta, content):
    try:
        item = dict()
        meta = json.loads(meta)
        # #print "META DUMP FAVOURITES %s" % meta
        try: id = meta['imdb']
        except: id = meta['tvdb']

        if 'title' in meta: title = item['title'] = meta['title']
        if 'tvshowtitle' in meta: title = item['title'] = meta['tvshowtitle']
        if 'year' in meta: item['year'] = meta['year']
        if 'poster' in meta: item['poster'] = meta['poster']
        if 'fanart' in meta: item['fanart'] = meta['fanart']
        if 'imdb' in meta: item['imdb'] = meta['imdb']
        if 'tmdb' in meta: item['tmdb'] = meta['tmdb']
        if 'tvdb' in meta: item['tvdb'] = meta['tvdb']
        if 'tvrage' in meta: item['tvrage'] = meta['tvrage']

        control.makeFile(dataPath)
        dbcon = database.connect(favouritesFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s (""id TEXT, ""items TEXT, ""UNIQUE(id)"");" % content)
        dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, id))
        dbcur.execute("INSERT INTO %s Values (?, ?)" % content, (id, repr(item)))
        dbcon.commit()

        # control.refresh()
        control.infoDialog('Added to Watchlist', heading=title, icon=item['poster'])
    except:
        return

def addEpisodes(meta, content):
    try:
        item = dict()
        meta = json.loads(meta)
        content = "episode"
        try: id = meta['imdb']
        except: id = meta['tvdb']

        if 'title' in meta: title = item['title'] = meta['title']
        if 'tvshowtitle' in meta: title = item['tvshowtitle'] = meta['tvshowtitle']
        if 'year' in meta: item['year'] = meta['year']
        if 'poster' in meta: item['poster'] = meta['poster']
        if 'fanart' in meta: item['fanart'] = meta['fanart']
        if 'imdb' in meta: item['imdb'] = meta['imdb']
        if 'tmdb' in meta: item['tmdb'] = meta['tmdb']
        if 'tvdb' in meta: item['tvdb'] = meta['tvdb']
        if 'tvrage' in meta: item['tvrage'] = meta['tvrage']
        if 'episode' in meta: item['episode'] = meta['episode']
        if 'season' in meta: item['season'] = meta['season']
        if 'premiered' in meta: item['premiered'] = meta['premiered']
        if 'original_year' in meta: item['original_year'] = meta['original_year']

        control.makeFile(dataPath)
        dbcon = database.connect(favouritesFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s (""id TEXT, ""items TEXT, ""UNIQUE(id)"");" % content)
        dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, id))
        dbcur.execute("INSERT INTO %s Values (?, ?)" % content, (id, repr(item)))
        dbcon.commit()

        # control.refresh()
        control.infoDialog('Added to Watchlist', heading=title, icon=item['poster'])
    except:
        return


def deleteFavourite(meta, content):
    try:
        meta = json.loads(meta)
        if 'title' in meta: title = meta['title']
        if 'tvshowtitle' in meta: title = meta['tvshowtitle']

        try:
            dbcon = database.connect(favouritesFile)
            dbcur = dbcon.cursor()
            try: dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, meta['imdb']))
            except: pass
            try: dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, meta['tvdb']))
            except: pass
            try: dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, meta['tmdb']))
            except: pass
            dbcon.commit()
        except:
            pass

        control.refresh()
        control.infoDialog('Removed From Watchlist', heading=title)
    except:
        return


def deleteProgress(meta, content):
    try:
        meta = json.loads(meta)
        try:
            dbcon = database.connect(progressFile)
            dbcur = dbcon.cursor()
            try: dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, meta['imdb']))
            except: pass
            try: dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, meta['tvdb']))
            except: pass
            try: dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, meta['tmdb']))
            except: pass
            dbcon.commit()
        except:
            pass

        control.refresh()

    except:
        return

