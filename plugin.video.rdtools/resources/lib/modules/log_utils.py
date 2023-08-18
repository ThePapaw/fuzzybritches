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

import time
import cProfile
import io
import pstats
import json
import xbmc
from resources.lib.modules import control
from xbmc import LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO, LOGNONE, LOGWARNING  # @UnusedImport

name = 'Real-Debrid Tools DEBUG'
def debug(msg, txt, level=LOGDEBUG):
    req_level = level
    if not control.setting('Real-Debrid Tools.debug') == 'true': return
    level = LOGDEBUG

    try:
        if isinstance(msg, str):
            msg = '%s (ENCODED)' % (msg)

        xbmc.log('[%s] >>> %s | %s' % (name, msg, txt), level)

    except Exception as e:
        try:
            xbmc.log('Logging Failure: %s' % (e), level)
        except:
            pass  # just give up



def log(msg, level=LOGDEBUG):
    req_level = level
    
    level = LOGDEBUG

    try:
        if isinstance(msg, str):
            msg = '%s (ENCODED)' % (msg)

        xbmc.log('[%s] >>> %s' % (name, msg), level)

    except Exception as e:
        try:
            xbmc.log('Logging Failure: %s' % (e), level)
        except:
            pass  # just give up


class Profiler(object):
    def __init__(self, file_path, sort_by='time', builtins=False):
        self._profiler = cProfile.Profile(builtins=builtins)
        self.file_path = file_path
        self.sort_by = sort_by

    def profile(self, f):
        def method_profile_on(*args, **kwargs):
            try:
                self._profiler.enable()
                result = self._profiler.runcall(f, *args, **kwargs)
                self._profiler.disable()
                return result
            except Exception as e:
                log('Profiler Error: %s' % (e), LOGWARNING)
                return f(*args, **kwargs)

        def method_profile_off(*args, **kwargs):
            return f(*args, **kwargs)

        if _is_debugging():
            return method_profile_on
        else:
            return method_profile_off

    def __del__(self):
        self.dump_stats()

    def dump_stats(self):
        if self._profiler is not None:
            s = io.StringIO()
            params = (self.sort_by,) if isinstance(self.sort_by, str) else self.sort_by
            ps = pstats.Stats(self._profiler, stream=s).sort_stats(*params)
            ps.print_stats()
            if self.file_path is not None:
                with open(self.file_path, 'w') as f:
                    f.write(s.getvalue())


def trace(method):
    def method_trace_on(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        log('{name!r} time: {time:2.4f}s args: |{args!r}| kwargs: |{kwargs!r}|'.format(name=method.__name__, time=end - start, args=args, kwargs=kwargs), LOGDEBUG)
        return result

    def method_trace_off(*args, **kwargs):
        return method(*args, **kwargs)

    if _is_debugging():
        return method_trace_on
    else:
        return method_trace_off


def _is_debugging():
    command = {'jsonrpc': '2.0', 'id': 1, 'method': 'Settings.getSettings', 'params': {'filter': {'section': 'system', 'category': 'logging'}}}
    js_data = execute_jsonrpc(command)
    for item in js_data.get('result', {}).get('settings', {}):
        if item['id'] == 'debug.showloginfo':
            return item['value']

    return False


def execute_jsonrpc(command):
    if not isinstance(command, str):
        command = json.dumps(command)
    response = control.jsonrpc(command)
    return json.loads(response)
