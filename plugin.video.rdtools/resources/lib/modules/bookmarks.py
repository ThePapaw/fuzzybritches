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

import re,sys,json,time,xbmc
import hashlib,urllib.request,urllib.parse,urllib.error,os,zlib,base64,codecs,xmlrpc.client


try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

from resources.lib.modules import control
from resources.lib.modules import cleantitle

class bookmarks:
    def getPlayer(self, name):
        try:
            offset = '0'

            if not control.setting('bookmarks') == 'true': raise Exception()
            idFile = cleantitle.get(name)

            dbcon = database.connect(control.bookmarksFile)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM bookmark WHERE idFile = '%s'" % idFile)
            match = dbcur.fetchone()
            self.offset = str(match[1])
            dbcon.commit()

            if self.offset == '0': raise Exception()
            
            # AUTO RESUME
            if control.setting('bookmarks.autoresume') == 'true': return self.offset

            minutes, seconds = divmod(float(self.offset), 60) ; hours, minutes = divmod(minutes, 60)
            label = '%02d:%02d:%02d' % (hours, minutes, seconds)
            label = (control.lang(32502) % label)

            try: yes = control.dialog.contextmenu([label, control.lang(32501), ])
            except: yes = control.yesnoDialog(label, '', '', str(name), control.lang(32503), control.lang(32501))

            if yes: self.offset = '0'

            return self.offset
        except:
            return offset
            
            
    def get(self, name):
        try:
            offset = '0'

            if not control.setting('bookmarks') == 'true': raise Exception()
            idFile = cleantitle.get(name)

            dbcon = database.connect(control.bookmarksFile)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM bookmark WHERE idFile = '%s'" % idFile)
            match = dbcur.fetchone()
            self.offset = str(match[1])
            dbcon.commit()

            if self.offset == '0' or self.offset == None: raise Exception()

            return self.offset
        except:
            return offset

    def reset(self, currentTime, totalTime, name):
        try:
            if not control.setting('bookmarks') == 'true': raise Exception()

            timeInSeconds = str(currentTime)
            ok = int(currentTime) > 180 and (currentTime / totalTime) <= .92

            idFile = cleantitle.get(name)

            control.makeFile(control.dataPath)
            dbcon = database.connect(control.bookmarksFile)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS bookmark (""idFile TEXT, ""timeInSeconds TEXT, ""UNIQUE(idFile)"");")
            dbcur.execute("DELETE FROM bookmark WHERE idFile = '%s'" % idFile)
            if ok: dbcur.execute("INSERT INTO bookmark Values (?, ?)", (idFile, timeInSeconds))
            dbcon.commit()
        except:
            pass

    def delete(self, name):
        try:
            
            if not control.setting('bookmarks') == 'true': raise Exception()
            idFile = cleantitle.get(name)

            control.makeFile(control.dataPath)
            dbcon = database.connect(control.bookmarksFile)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS bookmark (""idFile TEXT, ""timeInSeconds TEXT, ""UNIQUE(idFile)"");")
            dbcur.execute("DELETE FROM bookmark WHERE idFile = '%s'" % idFile)
            dbcon.commit()
        except:
            pass

