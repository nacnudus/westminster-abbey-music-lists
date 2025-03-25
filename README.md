# Westminster Abbey music lists

Fetch the records of past choral services.

```sh
curl https://www.westminster-abbey.org/Umbraco/Api/CustomData/AsyncUpdateServicesList?page=-1&target=8%2C3%2C5&site=0&location=&music=False&pagingInterval=Year&currentUrl=https%3A%2F%2Fwww.westminster-abbey.org%2Fworship-music%2Fservices-times%2Fchoral-services > 2024.json
jq --raw-output '.value' 2024.json > 2024.html

curl https://www.westminster-abbey.org/Umbraco/Api/CustomData/AsyncUpdateServicesList?page=-2&target=8%2C3%2C5&site=0&location=&music=False&pagingInterval=Year&currentUrl=https%3A%2F%2Fwww.westminster-abbey.org%2Fworship-music%2Fservices-times%2Fchoral-services > 2023.json
jq --raw-output '.value' 2023.json > 2023.html

curl https://www.westminster-abbey.org/Umbraco/Api/CustomData/AsyncUpdateServicesList?page=-3&target=8%2C3%2C5&site=0&location=&music=False&pagingInterval=Year&currentUrl=https%3A%2F%2Fwww.westminster-abbey.org%2Fworship-music%2Fservices-times%2Fchoral-services > 2022.json
jq --raw-output '.value' 2022.json > 2022.html
```

Then Use the script `html_table_to_json.py` to convert the HTML to JSON. The filenames are hardcoded because I'm lazy.

Then extract TSV records from the JSON files, one row per musical work that was sung.

```sh
cat 2024music.json | jq -r '.[] | . as $day | .services[] | . as $service | .music[] | [$day.date, $service.time, $service.title, $service.location, $service.notes, .] | @tsv' > 2024music.tsv
cat 2023music.json | jq -r '.[] | . as $day | .services[] | . as $service | .music[] | [$day.date, $service.time, $service.title, $service.location, $service.notes, .] | @tsv' > 2023music.tsv
cat 2022music.json | jq -r '.[] | . as $day | .services[] | . as $service | .music[] | [$day.date, $service.time, $service.title, $service.location, $service.notes, .] | @tsv' > 2022music.tsv
```
