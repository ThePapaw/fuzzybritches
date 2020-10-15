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


class Cloudflare_Loop_Protection(Exception):
    """
    Raise error for recursive depth protection
    """


class Cloudflare_Block(Exception):
    """
    Raise error for Cloudflare 1020 block
    """


class Cloudflare_Error_IUAM(Exception):
    """
    Raise error for problem extracting IUAM paramters from Cloudflare payload
    """


class Cloudflare_Error_reCaptcha(Exception):
    """
    Raise error for problem extracting reCaptcha paramters from Cloudflare payload
    """


class Cloudflare_reCaptcha_Provider(Exception):
    """
    Raise error for reCaptcha from Cloudflare, no provider loaded.
    """
