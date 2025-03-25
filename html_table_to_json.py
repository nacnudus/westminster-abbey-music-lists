import json

from itertools import batched
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("2023.html", encoding="utf8"), "html5lib")

table = soup.select_one("table")

children = [child for child in table.children if child.name is not None]

def day(tag):
    return {
        "date": tag.find("th", class_="large").text,
        "annotations": [
            small.text.strip() for small in tag.find_all("th", class_="small")
        ],
        "services": []
    }


def service(tag):
    return {
        "time": tag.find("td", class_="serviceListingTime").text.strip(),
        "title": tag.find("td", class_="serviceListingTitle").text.strip(),
        "location": tag.find("td", class_="serviceListingLocation").text.strip(),
        "notes": tag.find("td", class_="serviceListingNotes").text.strip(),
        "music": music(tag.find("td", class_="serviceListingMusic")),
    }
    return tag


def music(tag):
    # Use only the first paragraph. A second paragraph is a preacher.
    if tag.p:
        music = tag.p
    else:
        music = tag

    soup = BeautifulSoup(str(music), "html5lib")

    for br in soup('br'):
        br.replace_with('\n')

    lines =  str(soup.body).split("\n")
    works = [
        BeautifulSoup(line, "html5lib").get_text(strip=False).replace(u"\xa0", " ") for line in lines
    ]
    return list(filter(len, works))


days = []
services = []
for child in children:
    match child.name:
        case "thead":
            current_day = day(child)
            days.append(current_day)
        case "tbody":
            current_day["services"].append(service(child))

days[0]

with open('2023music.json', 'w', encoding='utf-8') as f:
    json.dump(days, f, ensure_ascii=False, indent=4)
