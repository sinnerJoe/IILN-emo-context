
import requests
import json
import pyquery


def create_dict():
    content = requests.get(
        "https://www.utf8-chartable.de/unicode-utf8-table.pl?start=9728").text

    dom =  pyquery.PyQuery(bytes(content, "utf-8"))
    rows = dom.find("table.codetable tr")[1:]
    entries = dict()
    print(dir(rows[0]))
    for line in rows:
        char = line.getchildren()[1].text
        name = line.getchildren()[3].text
        entries[char] = name

    with open("emoji_dictionary.json", "wt", encoding = "utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)



def transform_emojis():
    emojis = None
    with open("emoji_dictionary.json", "rb") as f:
        emojis = json.load(f, encoding="utf-8")
    for key in emojis: 
        emojis[key] = "<" + emojis[key].replace(" ", "_") + ">"
    
    with open("emoji_dictionary.json", "wt", encoding="utf-8") as f:
        json.dump(emojis, f, ensure_ascii=False, indent=2)

create_dict()
transform_emojis()