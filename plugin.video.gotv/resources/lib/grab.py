import requests

def grab(code):
    url = "https://ustvgo.tv/player.php?stream=" + code
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
        'Referer': 'https://ustvgo.tv/'
    }
    r = requests.get(url, headers=headers).text.replace('\n', '').split("var hls_src='")[1].split("'")[0]
    return r
