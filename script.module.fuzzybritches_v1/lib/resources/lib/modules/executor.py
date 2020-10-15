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

import concurrent.futures
from itertools import islice
import xbmc
import threading

Executor = concurrent.futures.ThreadPoolExecutor


def execute(f, iterable, stop_flag=None, workers=10, timeout = 30):
    with Executor(max_workers=workers) as executor:
        threading.Timer(timeout, stop_flag.set)
        for future in _batched_pool_runner(executor, workers, f, iterable):

            if xbmc.abortRequested:
                break
            if stop_flag and stop_flag.isSet():
                break
            yield future.result()


def _batched_pool_runner(pool, batch_size, f, iterable):
    it = iter(iterable)

    # Submit the first batch of tasks.
    futures = set(pool.submit(f, x) for x in islice(it, batch_size))

    while futures:
        done, futures = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

        # Replenish submitted tasks up to the number that completed.
        futures.update(pool.submit(f, x) for x in islice(it, len(done)))

        for d in done:
            yield d