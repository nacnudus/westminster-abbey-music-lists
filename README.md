# Westminster Abbey music lists

Fetch the records of past choral services. The first year of data is 2020.

```sh
curl https://www.westminster-abbey.org/Umbraco/Api/CustomData/AsyncUpdateServicesList?page=-1&target=8%2C3%2C5&site=0&location=&music=False&pagingInterval=Year&currentUrl=https%3A%2F%2Fwww.westminster-abbey.org%2Fworship-music%2Fservices-times%2Fchoral-services > 2024.json
jq --raw-output '.value' 2024.json > 2024.html
```

Then Use the script `html_table_to_json.py` to convert the HTML to JSON. The filenames are hardcoded because I'm lazy.

Then extract TSV records from the JSON files, one row per musical work that was sung.

```sh
cat 2024music.json | jq -r '.[] | . as $day | .services[] | . as $service | .music[] | [$day.date, $service.time, $service.title, $service.location, $service.notes, .] | @tsv' > 2024music.tsv
```

## Old service sheets

Fetch a list of URLs from the Wayback Machine API

```
curl "http://web.archive.org/cdx/search/cdx?url=www.westminster-abbey.org/order-of-service?id=*&filter=statuscode:200&collapse=urlkey&fl=timestamp,original" > archive-urls.txt
awk '{print "http://web.archive.org/web/" $1 "/" $2}' archive-urls.txt > snapshot-urls.txt
```

```
mkdir -p snapshots
while read -r url; do
    [[ -z "$url" ]] && continue

    # Extract the id value from the URL (e.g., 10051)
    id=$(echo "$url" | sed -n 's/.*[?&]id=\([0-9]*\).*/\1/p')

    # Fallback if no ID is found in the URL
    if [[ -z "$id" ]]; then
        id="unknown_$(date +%s%N)"
    fi

    # Download the URL and save it as id.html
    curl -s "$url" -o "snapshots/${id}.html"
    echo "Downloaded: ${id}.html"

    # Be polite to the Wayback Machine servers
    sleep 1
done < snapshot-urls.txt
```

Extract the service date and time

```
for f in *.html; do
  [ -f "$f" ] || continue
  # Extract header and date/time lines using xidel
  header=$(xidel "$f" --css '.serviceHeader h1' 2>/dev/null)
  datetime_raw=$(xidel "$f" --css '.serviceDateTime' 2>/dev/null | paste -sd ' ' -)

  # Clean ordinal suffix (e.g., "2nd" -> "2") and convert to ISO 8601 UTC via GNU date
  cleaned_dt=$(echo "$datetime_raw" | sed -E 's/([0-9]+)(st|nd|rd|th)/\1/')
  utc_time=$(date -u -d "$cleaned_dt" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null)

  printf "%s | %s | %s\n" "$f" "$utc_time" "$header"
done
```
