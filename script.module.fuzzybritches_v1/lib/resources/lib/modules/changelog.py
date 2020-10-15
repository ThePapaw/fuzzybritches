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

def get():

        import xbmc,xbmcgui,xbmcaddon,xbmcvfs,os
        addonInfo = xbmcaddon.Addon().getAddonInfo
        addonPath = xbmc.translatePath(addonInfo('path'))
        changelogfile = os.path.join(addonPath, 'changelog.txt')
        r = open(changelogfile)
        text = r.read()

        id = 10147
        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(500)
        win = xbmcgui.Window(id)
        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                retry -= 1
                win.getControl(1).setLabel('Fuzzy Britches Version: %s' %(xbmcaddon.Addon().getAddonInfo('version')))
                win.getControl(5).setText(text)
                return
            except:
                pass
