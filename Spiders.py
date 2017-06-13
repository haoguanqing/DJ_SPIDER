from bs4 import BeautifulSoup as Soup

import urllib.request as req
import json
import socket
import sys

# 10 second default global timeout
socket.setdefaulttimeout(10)

HTML_PARSER = 'html.parser'
LXML_PARSER = 'lxml'


def martingarrix():
    name = 'Martin Garrix'
    image_urls = []
    url = 'http://www.martingarrix.com/'

    request_url = 'http://www.martingarrix.com/pkg/lt3-api/3.0/api/bandsintown/artists/events?name=Martin+Garrix&limit=50'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/59.0.3071.86 Safari/537.3',
               'Referer': 'http://www.martingarrix.com/tour'}
    response = req.urlopen(req.Request(request_url, None, headers))
    soup = Soup(response.read(), LXML_PARSER)
    events = json.loads(soup.find_all('p')[0].string)
    for event in events:
        venue = event['venue']['name']
        description = event['description']
        location = event['formatted_location']
        date = event['formatted_datetime']
        ticket_url = event['ticket_url']
        image_url = event['artists'][0]['image_url']
        thumb_url = event['artists'][0]['thumb_url']

    report(name)


def dimitrivegasandlikemike():
    name = 'Dimitri Vegas & Like Mike'
    image_urls = ['http://www.dimitrivegasandlikemike.com/img/%s.jpg' % x for x in range(6)]
    url = 'http://www.dimitrivegasandlikemike.com/'

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) Chrome/58.0.3029.110 Safari/10.1.1'}
    soup = Soup(req.urlopen(req.Request(url, None, headers)).read(), HTML_PARSER)

    events_list = soup.find_all('div', {'id': 'tourtitem', 'class': 'tourtitem'})
    for event in events_list:
        data = list(event.contents[0].children)
        venue = data[0].string
        location = data[1].string
        date = data[2].string

    report(name)


def dondiablo():
    name = 'Don Diablo'
    url = 'https://www.dondiablo.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) Chrome/58.0.3029.110 Safari/10.1.1'}
    soup = Soup(req.urlopen(req.Request(url, None, headers)).read(), HTML_PARSER)

    image_urls = [soup.find('img', {'class': 'load-false', 'name': '', 'data-type': 'image'})["data-image"]]

    # TODO crawl tour events
    report(name)


def report(task):
    print('Finished: ' + str(task))


def main():
    dondiablo()
    martingarrix()
    dimitrivegasandlikemike()


class Data(object):
    def __init__(self, name, url, image_url):
        self.name = name
        self.url = url
        self.image_url = image_url
        self.events = []


class Event(object):
    def __init__(self, date, tour_name, location, ticket_link):
        self.date = date
        self.tour_name = tour_name
        self.location = location
        self.ticket_link = ticket_link

if __name__ == '__main__':
    sys.exit(main())

