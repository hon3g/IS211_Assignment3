import argparse
import csv
import datetime
import re
import sys
import urllib.request


def download_data(url):
    response = urllib.request.urlopen(url)
    with open('weblog.csv', 'w') as file:
        file.write(response.read().decode('utf-8'))


def process_data():
    with open('weblog.csv', 'r') as file:
        csv_reader = csv.reader(file)
        log = list(csv_reader)
    return log


def search_image_hits(log):
    count = 0
    for i in log:
        if re.search(r'\.jpg$|'
                     r'\.gif$|'
                     r'\.png$'
                     ,i[0], re.IGNORECASE):
            count += 1
    image_pct = round(count / len(log) * 100, 1)
    print(f'Image requests account for {image_pct}% of all requests')


def find_most_popular_browser(log):
    browser_d = {
        'Firefox': 0
        ,'Chrome': 0
        ,'Safari': 0
        ,'Internet Explorer': 0
    }
    for i in log:
        if re.search('Gecko.+Firefox', i[2]):
            browser_d['Firefox'] += 1
        elif re.search('Chrome.+Safari', i[2]):
            browser_d['Chrome'] += 1
        elif re.search('AppleWebKit.+Safari', i[2]):
            browser_d['Safari'] += 1
        elif re.search('Windows NT', i[2], re.IGNORECASE) or \
                re.search('MSIE.+(Windows|Macintosh)', i[2]):
            browser_d['Internet Explorer'] += 1

    browser = max(browser_d, key=browser_d.get)
    print(f'{browser} is the most popular browser of the day')


def get_hits_by_hour(log):
    hour_d = dict()
    for i in log:
        dt = datetime.datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S')
        hour = dt.hour
        if hour not in hour_d:
            hour_d[hour] = 0
        hour_d[hour] += 1
    for h, n in hour_d.items():
        print(f'Hour {h:02d} has {n} hits')


def main(url):
    print(f"Running main with URL = {url}...")
    try:
        download_data(url)
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit()

    weblog = process_data()
    search_image_hits(weblog)
    find_most_popular_browser(weblog)
    get_hits_by_hour(weblog)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
