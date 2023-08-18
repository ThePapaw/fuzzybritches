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

import threading


class Thread(threading.Thread):
    def __init__(self, target, *args):
        self.target = target
        self.args = args
        threading.Thread.__init__(self)
    def run(self):
        self.target(*self.args)

