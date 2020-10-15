import sys, urllib, contextlib
try:
    import simplejson as json
except ImportError:
    import json

# get user defined apikey
import xbmcaddon
__addon__ = xbmcaddon.Addon()
API_KEY = __addon__.getSetting("fanarttv_key") or "ed4b784f97227358b31ca4dd966a04f1"

API_URL_TV = 'http://webservice.fanart.tv/v3/tv/%s?api_key=%s'

class FanartTV(object):
    def __init__(self):
        pass

    @staticmethod
    def find_artwork(tvdb_id, art_type, lang = 'en'):
        # We need both clearlogo and hdtvlogo for clearlogo. Otherwise tvposter or tvbanner.
        if art_type == 'clearlogo':
            find_types = [ 'hdtvlogo', 'clearlogo' ]
        else:
            find_types = [ 'tv' + art_type ]
        ret = None
        url = API_URL_TV % (tvdb_id, API_KEY)
        with contextlib.closing(urllib.urlopen(url)) as udata:
            if udata:
                data = json.load(udata)
                if data:
                    for find in find_types:
                        logos = data.get(find, [])
                        for logo in logos:
                            if logo['lang'] == lang:
                                return logo['url']
                            # We'll accept the wrong language as a fallback, as they are sometimes mislabeled.
                            if not ret:
                                ret = logo['url']
        return ret

# Some helper code to check on the data to see how our queries are working.
if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stdout.write("%s\n" % FanartTV.find_artwork(83462, 'clearlogo'))
    else:
        sys.stdout.write("%s\n" % FanartTV.find_artwork(sys.argv[1], sys.argv[2]))

# vim: sw=4 ts=8 et
