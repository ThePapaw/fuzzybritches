import os, re, sys, urllib, time

COUNTRY_DB = 'country.db'
COUNTRY_DB_VER = 1

# updated 01/31/2020 // --zones
COUNTRY_ZONES = {
    'afghanistan': 'Asia/Kabul',
    'aland islands': 'Europe/Mariehamn',
    'albania': 'Europe/Tirane',
    'algeria': 'Africa/Algiers',
    'american samoa': 'Pacific/Pago_Pago',
    'andorra': 'Europe/Andorra',
    'angola': 'Africa/Luanda',
    'anguilla': 'America/Anguilla',
    'antigua and barbuda': 'America/Antigua',
    'argentina': 'America/Argentina/Ushuaia',
    'armenia': 'Asia/Yerevan',
    'aruba': 'America/Aruba',
    'australia': 'Australia/Sydney',
    'austria': 'Europe/Vienna',
    'azerbaijan': 'Asia/Baku',
    'bahamas': 'America/Nassau',
    'bahrain': 'Asia/Bahrain',
    'bangladesh': 'Asia/Dhaka',
    'barbados': 'America/Barbados',
    'belarus': 'Europe/Minsk',
    'belgium': 'Europe/Brussels',
    'belize': 'America/Belize',
    'benin': 'Africa/Porto-Novo',
    'bermuda': 'Atlantic/Bermuda',
    'bhutan': 'Asia/Thimphu',
    'bolivia': 'America/La_Paz',
    'bonaire, saint eustatius and saba': 'America/Kralendijk',
    'bosnia and herzegovina': 'Europe/Sarajevo',
    'botswana': 'Africa/Gaborone',
    'brazil': 'America/Noronha',
    'british indian ocean territory': 'Indian/Chagos',
    'british virgin islands': 'America/Tortola',
    'brunei': 'Asia/Brunei',
    'bulgaria': 'Europe/Sofia',
    'burkina faso': 'Africa/Ouagadougou',
    'burundi': 'Africa/Bujumbura',
    'cabo verde': 'Atlantic/Cape_Verde',
    'cambodia': 'Asia/Phnom_Penh',
    'cameroon': 'Africa/Douala',
    'canada': 'America/Moncton',
    'cayman islands': 'America/Cayman',
    'central african republic': 'Africa/Bangui',
    'chad': 'Africa/Ndjamena',
    'chile': 'America/Santiago',
    'china': 'Asia/Shanghai',
    'christmas island': 'Indian/Christmas',
    'cocos islands': 'Indian/Cocos',
    'colombia': 'America/Bogota',
    'comoros': 'Indian/Comoro',
    'cook islands': 'Pacific/Rarotonga',
    'costa rica': 'America/Costa_Rica',
    'croatia': 'Europe/Zagreb',
    'cuba': 'America/Havana',
    'curacao': 'America/Curacao',
    'cyprus': 'Asia/Nicosia',
    'czechia': 'Europe/Prague',
    'democratic republic of the congo': 'Africa/Lubumbashi',
    'denmark': 'Europe/Copenhagen',
    'djibouti': 'Africa/Djibouti',
    'dominica': 'America/Dominica',
    'dominican republic': 'America/Santo_Domingo',
    'ecuador': 'America/Guayaquil',
    'egypt': 'Africa/Cairo',
    'el salvador': 'America/El_Salvador',
    'equatorial guinea': 'Africa/Malabo',
    'eritrea': 'Africa/Asmara',
    'estonia': 'Europe/Tallinn',
    'eswatini': 'Africa/Mbabane',
    'ethiopia': 'Africa/Addis_Ababa',
    'falkland islands': 'Atlantic/Stanley',
    'faroe islands': 'Atlantic/Faroe',
    'fiji': 'Pacific/Fiji',
    'finland': 'Europe/Helsinki',
    'france': 'Europe/Paris',
    'french guiana': 'America/Cayenne',
    'french polynesia': 'Pacific/Gambier',
    'french southern territories': 'Indian/Kerguelen',
    'gabon': 'Africa/Libreville',
    'gambia': 'Africa/Banjul',
    'georgia': 'Asia/Tbilisi',
    'germany': 'Europe/Busingen',
    'ghana': 'Africa/Accra',
    'gibraltar': 'Europe/Gibraltar',
    'greece': 'Europe/Athens',
    'greenland': 'America/Danmarkshavn',
    'grenada': 'America/Grenada',
    'guadeloupe': 'America/Guadeloupe',
    'guam': 'Pacific/Guam',
    'guatemala': 'America/Guatemala',
    'guernsey': 'Europe/Guernsey',
    'guinea': 'Africa/Conakry',
    'guinea-bissau': 'Africa/Bissau',
    'guyana': 'America/Guyana',
    'haiti': 'America/Port-au-Prince',
    'honduras': 'America/Tegucigalpa',
    'hong kong': 'Asia/Hong_Kong',
    'hungary': 'Europe/Budapest',
    'iceland': 'Atlantic/Reykjavik',
    'india': 'Asia/Kolkata',
    'indonesia': 'Asia/Jayapura',
    'iran': 'Asia/Tehran',
    'iraq': 'Asia/Baghdad',
    'ireland': 'Europe/Dublin',
    'isle of man': 'Europe/Isle_of_Man',
    'israel': 'Asia/Jerusalem',
    'italy': 'Europe/Rome',
    'ivory coast': 'Africa/Abidjan',
    'jamaica': 'America/Jamaica',
    'japan': 'Asia/Tokyo',
    'jersey': 'Europe/Jersey',
    'jordan': 'Asia/Amman',
    'kazakhstan': 'Asia/Qostanay',
    'kenya': 'Africa/Nairobi',
    'kiribati': 'Pacific/Kiritimati',
    'kuwait': 'Asia/Kuwait',
    'kyrgyzstan': 'Asia/Bishkek',
    'laos': 'Asia/Vientiane',
    'latvia': 'Europe/Riga',
    'lebanon': 'Asia/Beirut',
    'lesotho': 'Africa/Maseru',
    'liberia': 'Africa/Monrovia',
    'libya': 'Africa/Tripoli',
    'liechtenstein': 'Europe/Vaduz',
    'lithuania': 'Europe/Vilnius',
    'luxembourg': 'Europe/Luxembourg',
    'macao': 'Asia/Macau',
    'madagascar': 'Indian/Antananarivo',
    'malawi': 'Africa/Blantyre',
    'malaysia': 'Asia/Kuching',
    'maldives': 'Indian/Maldives',
    'mali': 'Africa/Bamako',
    'malta': 'Europe/Malta',
    'marshall islands': 'Pacific/Majuro',
    'martinique': 'America/Martinique',
    'mauritania': 'Africa/Nouakchott',
    'mauritius': 'Indian/Mauritius',
    'mayotte': 'Indian/Mayotte',
    'mexico': 'America/Cancun',
    'micronesia': 'Pacific/Pohnpei',
    'moldova': 'Europe/Chisinau',
    'monaco': 'Europe/Monaco',
    'mongolia': 'Asia/Ulaanbaatar',
    'montenegro': 'Europe/Podgorica',
    'montserrat': 'America/Montserrat',
    'morocco': 'Africa/Casablanca',
    'mozambique': 'Africa/Maputo',
    'myanmar': 'Asia/Yangon',
    'namibia': 'Africa/Windhoek',
    'nauru': 'Pacific/Nauru',
    'nepal': 'Asia/Kathmandu',
    'netherlands': 'Europe/Amsterdam',
    'new caledonia': 'Pacific/Noumea',
    'new zealand': 'Pacific/Chatham',
    'nicaragua': 'America/Managua',
    'niger': 'Africa/Niamey',
    'nigeria': 'Africa/Lagos',
    'niue': 'Pacific/Niue',
    'norfolk island': 'Pacific/Norfolk',
    'north korea': 'Asia/Pyongyang',
    'north macedonia': 'Europe/Skopje',
    'northern mariana islands': 'Pacific/Saipan',
    'norway': 'Europe/Oslo',
    'oman': 'Asia/Muscat',
    'pakistan': 'Asia/Karachi',
    'palau': 'Pacific/Palau',
    'palestinian territory': 'Asia/Hebron',
    'panama': 'America/Panama',
    'papua new guinea': 'Pacific/Bougainville',
    'paraguay': 'America/Asuncion',
    'peru': 'America/Lima',
    'philippines': 'Asia/Manila',
    'pitcairn': 'Pacific/Pitcairn',
    'poland': 'Europe/Warsaw',
    'portugal': 'Europe/Lisbon',
    'puerto rico': 'America/Puerto_Rico',
    'qatar': 'Asia/Qatar',
    'republic of the congo': 'Africa/Brazzaville',
    'reunion': 'Indian/Reunion',
    'romania': 'Europe/Bucharest',
    'russia': 'Asia/Kamchatka',
    'rwanda': 'Africa/Kigali',
    'saint barthelemy': 'America/St_Barthelemy',
    'saint helena': 'Atlantic/St_Helena',
    'saint kitts and nevis': 'America/St_Kitts',
    'saint lucia': 'America/St_Lucia',
    'saint martin': 'America/Marigot',
    'saint pierre and miquelon': 'America/Miquelon',
    'saint vincent and the grenadines': 'America/St_Vincent',
    'samoa': 'Pacific/Apia',
    'san marino': 'Europe/San_Marino',
    'sao tome and principe': 'Africa/Sao_Tome',
    'saudi arabia': 'Asia/Riyadh',
    'senegal': 'Africa/Dakar',
    'serbia': 'Europe/Belgrade',
    'seychelles': 'Indian/Mahe',
    'sierra leone': 'Africa/Freetown',
    'singapore': 'Asia/Singapore',
    'sint maarten': 'America/Lower_Princes',
    'slovakia': 'Europe/Bratislava',
    'slovenia': 'Europe/Ljubljana',
    'solomon islands': 'Pacific/Guadalcanal',
    'somalia': 'Africa/Mogadishu',
    'south africa': 'Africa/Johannesburg',
    'south georgia and the south sandwich islands': 'Atlantic/South_Georgia',
    'south korea': 'Asia/Seoul',
    'south sudan': 'Africa/Juba',
    'spain': 'Europe/Madrid',
    'sri lanka': 'Asia/Colombo',
    'sudan': 'Africa/Khartoum',
    'suriname': 'America/Paramaribo',
    'svalbard and jan mayen': 'Arctic/Longyearbyen',
    'sweden': 'Europe/Stockholm',
    'switzerland': 'Europe/Zurich',
    'syria': 'Asia/Damascus',
    'taiwan': 'Asia/Taipei',
    'tajikistan': 'Asia/Dushanbe',
    'tanzania': 'Africa/Dar_es_Salaam',
    'thailand': 'Asia/Bangkok',
    'timor leste': 'Asia/Dili',
    'togo': 'Africa/Lome',
    'tokelau': 'Pacific/Fakaofo',
    'tonga': 'Pacific/Tongatapu',
    'trinidad and tobago': 'America/Port_of_Spain',
    'tunisia': 'Africa/Tunis',
    'turkey': 'Europe/Istanbul',
    'turkmenistan': 'Asia/Ashgabat',
    'turks and caicos islands': 'America/Grand_Turk',
    'tuvalu': 'Pacific/Funafuti',
    'u.s. virgin islands': 'America/St_Thomas',
    'uganda': 'Africa/Kampala',
    'uk': 'Europe/London',
    'ukraine': 'Europe/Zaporozhye',
    'united arab emirates': 'Asia/Dubai',
    'united kingdom': 'Europe/London',
    'united states': 'America/New_York',
    'uruguay': 'America/Montevideo',
    'usa': 'America/New_York',
    'uzbekistan': 'Asia/Tashkent',
    'vanuatu': 'Pacific/Efate',
    'vatican': 'Europe/Vatican',
    'venezuela': 'America/Caracas',
    'vietnam': 'Asia/Ho_Chi_Minh',
    'wallis and futuna': 'Pacific/Wallis',
    'western sahara': 'Africa/El_Aaiun',
    'yemen': 'Asia/Aden',
    'zambia': 'Africa/Lusaka',
    'zimbabwe': 'Africa/Harare',
    'unknown': 'UTC',
}


class CountryLookup(object):
    def __init__(self):
        import requests
        from bs4 import BeautifulSoup
        self.country_dict = {}
        with requests.Session() as s:
            for i in range(1, 29):
                url = "https://www.thetvdb.com/networks?page=%s" % i
                response = s.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                print "Loading: %s" % (url)
                for tr in soup.find_all('tr')[1:]:
                    tds = tr.find_all('td')
                    country = tds[2].get_text(strip=True)
                    # fix tvdb mapping name so it aligns with our zone map
                    if country == u'United States of America':
                        country = u'United States'
                    elif country == u'The Netherlands':
                        country = u'Netherlands'
                    elif country == u'Great Britain':
                        country = u'United Kingdom'
                    elif country == u'Swiss Confederation':
                        country = u'Switzerland'
                    elif country == u'Czech Republic':
                        country = u'Czechia'
                    self.country_dict[tds[0].get_text(strip=True)] = country
                    #print "'%s': '%s'" % (tds[0].text.encode('utf-8').strip(), tds[2].text.encode('utf-8').strip())
                time.sleep(1)

            # default country which defaults to UTC
            self.country_dict[''] = u'Unknown'
            print "Scraped %s networks from tvdb" % (len(self.country_dict)-1)
            if len(self.country_dict) < 50:
                raise Exception("Country data was not parsed correctly.")

    def get_country_dict(self):
        return self.country_dict

    @staticmethod
    def get_country_timezone(country):
        return COUNTRY_ZONES.get(country.lower(), None)

    @staticmethod
    def get_zones():
        url = 'http://download.geonames.org/export/dump/countryInfo.txt'
        iso_map = {}
        data = urllib.urlopen(url)
        for line in data:
            if line.startswith("#"):
                continue
            iso, iso3, iso_num, fips, country, extra = line.split("\t", 5)
            iso_map[iso] = country.lower().strip()

        url = 'http://download.geonames.org/export/dump/timeZones.txt'
        zone_map = {}
        data = urllib.urlopen(url)
        for line in data:
            iso, tz_id, goff1, goff2, goff3 = line.split("\t")
            if tz_id in ("Pacific/Easter", "America/St_Johns") or iso in ('AQ', 'UM'):
                continue
            country = iso_map.get(iso, False)
            if country:
                goff1 = float(goff1)
                if country in zone_map and zone_map[country][0] > goff1:
                    continue
                zone_map[country] = (goff1, tz_id)

        for country in zone_map:
            zone_map[country] = zone_map[country][1]

        # Allow some country aliases.
        zone_map['usa'] = zone_map['united states']
        zone_map['uk'] = zone_map['united kingdom']

        return zone_map


# Some helper code to check on the data and output a new timezone list.
def main(argv):
    import getopt

    try:
        opts, args = getopt.getopt(argv, "h", ["map", "zones", "test", "save", "help"])
    except getopt.GetoptError:
        usage()
    if not opts:
        opts.append(('--test', ''))
    for opt, arg in opts:
        if opt == "--map":
            c = CountryLookup()
            cd = c.get_country_dict()
            del cd['']
            prettify('', c.get_country_dict(), ",", "    '': 'Unknown',\n")
        elif opt == "--zones":
            prettify("COUNTRY_ZONES = ", CountryLookup.get_zones(), "',", "    'unknown': 'UTC',\n")
        elif opt == "--test":
            resources_lib_re = re.compile(r"[^a-z]+resources[^a-z]+lib$")
            sys.path.insert(0, resources_lib_re.sub("", sys.path[0]))
            from dateutil import zoneinfo

            tried = {}
            saw_error = False
            for country, zone in COUNTRY_ZONES.iteritems():
                if zone not in tried:
                    x = zoneinfo.gettz(zone)
                    if x is None:
                        # To fix this, we'll need new data from http://www.twinsun.com/tz/tz-link.htm
                        sys.stdout.write("Timezone %s is not available in the dateutil zoneinfo tar file!!!\n" % zone)
                        saw_error = True
                    tried[zone] = 1
            if saw_error:
                sys.stdout.write("^-- Visit http://www.twinsun.com/tz/tz-link.htm for updated info.\n")
            else:
                sys.stdout.write("All the listed timezone names were found in the zoneinfo tar file.\n")

            c = CountryLookup()
            saw_error = False
            for station, country in c.get_country_dict().iteritems():
                zone = COUNTRY_ZONES.get(country.lower(), None)
                if zone is None:
                    sys.stdout.write("Missing country timezone for %s\n" % country)
                    saw_error = True
            if saw_error:
                sys.stdout.write("^-- Run with --zones to output a new country table.\n")
            else:
                sys.stdout.write("All needed country names were found.\n")
        elif opt == "--save":
            c = CountryLookup()
            cd = c.get_country_dict()
            #path = os.path.join(__datapath__, COUNTRY_DB)
            file(COUNTRY_DB, "w").write(repr([cd, COUNTRY_DB_VER, time.time()]))
        elif opt in ("-h", "--help"):
            usage()
        else:
            sys.exit(42) # Impossible...


def prettify(prefix, obj, line_end, suffix):
    lines = ("    " + repr(obj).strip("{}").replace(line_end+" ", line_end+"\n    ") + ",").splitlines()
    lines.sort()
    sys.stdout.write("%s{\n%s\n%s}\n" % (prefix, "\n".join(lines), suffix))
    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(networks)


def usage():
    sys.stderr.write("country_lookup.py [--map] [--zones] [--test] [--save] [--help]\n")
    sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])