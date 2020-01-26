import json
import re
import urllib.request


CF_COMPONENT_URL = "https://yh6f0r4529hb.statuspage.io/api/v2/components.json"
CF_IGNORE_ID = {
    "1km35smx8p41",
}

CF_DATA_TMPL = """\
    "{iata}" => array(
        "iata" => "{iata}",
        "city" => "{city}",
        "state" => "{state}",
        "country" => "{country}",
        "alpha2" => "{alpha2}",
    ),
"""

ISO3166_URL = (
    "https://github.com/flyingcircusio/pycountry"
    "/raw/master/src/pycountry/databases/iso3166-1.json"
)

print("Downloading Cloudflare status components.json")
components = json.loads(urllib.request.urlopen(CF_COMPONENT_URL).read())

special_case_iata_country = {
    "ZDM": {"country": "Palestine", "alpha2": "PS"},
    "HKG": {"country": "Hong Kong"},
    "MFM": {"country": "China"},
    "TPE": {"country": "Taiwan"},
    "MPM": {"country": "Mozambique"},
    "DME": {"alpha2": "RU"},
    "LED": {"alpha2": "RU"},
    "ICN": {"alpha2": "KR"},
    "NOU": {"country": "New Caledonia"},
    "RIC": {"state": "VA", "country": "United States"},
}

try:
    with open("iso3166-1.json", "r") as file:
        iso3166 = json.load(file)["3166-1"]
    print("Using local iso3166-1.json")
except FileNotFoundError:
    print("Downloading remote iso3166-1.json from pycountry repo")
    iso3166 = json.loads(urllib.request.urlopen(ISO3166_URL).read())["3166-1"]


with open("Upload/inc/plugins/cloudflare-cfray/cfray_data.php", "w+") as file:
    file.write("<?php\n$cfray_data = array(\n")

    total = 0
    regex = re.compile(r",\s*|\s*-\s*\(")

    for component_id in CF_IGNORE_ID:
        print("Ignoring component with ID/Group ID:", component_id)

    for value in components["components"]:
        if value["id"] not in CF_IGNORE_ID and value["group_id"] not in CF_IGNORE_ID:
            data = regex.split(value["name"])
            data[-1] = data[-1].strip("()")
            iata = {
                "iata": "",
                "city": "",
                "state": "",
                "country": "",
                "alpha2": "",
            }
            data_len = len(data)
            if data_len == 2:
                iata["city"], iata["iata"] = data
            elif data_len == 3:
                iata["city"], iata["country"], iata["iata"] = data
            elif data_len == 4:
                iata["city"], iata["state"], iata["country"], iata["iata"] = data
            else:
                print("Skipping component:", value["name"], "| ID:", value["id"])
                continue

            case = special_case_iata_country.get(iata["iata"], None)
            if case:
                iata = {**iata, **case}

            for entry in iso3166:
                if (
                    entry["name"] == iata["country"]
                    or entry.get("common_name", "") == iata["country"]
                    or entry.get("official_name", "") == iata["country"]
                ):
                    iata["alpha2"] = entry["alpha_2"]

            if not iata["alpha2"]:
                print("Can't find Alpha-2 entry:", iata)

            file.write(CF_DATA_TMPL.format(**iata))
            total += 1

    file.write(");")

print("Total CF-Ray/IATA/Data center:", total)
