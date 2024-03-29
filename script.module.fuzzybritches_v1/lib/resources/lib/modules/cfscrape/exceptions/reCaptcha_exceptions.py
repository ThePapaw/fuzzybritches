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


class reCaptcha_Service_Unavailable(Exception):
    """
    Raise error for external services that cannot be reached
    """


class reCaptcha_Error_From_API(Exception):
    """
    Raise error for error from API response.
    """


class reCaptcha_Account_Error(Exception):
    """
    Raise error for reCaptcha provider account problem.
    """


class reCaptcha_Timeout(Exception):
    """
    Raise error for reCaptcha provider taking too long.
    """


class reCaptcha_Bad_Parameter(NotImplementedError):
    """
    Raise error for bad or missing Parameter.
    """


class reCaptcha_Bad_Job_ID(Exception):
    """
    Raise error for invalid job id.
    """


class reCaptcha_Report_Error(Exception):
    """
    Raise error for reCaptcha provider unable to report bad solve.
    """


class reCaptcha_Import_Error(Exception):
    """
    Raise error for reCaptcha, cannot import a module.
    """
