# -*- coding: utf-8 -*-
"""The first script in The Beatles Songs Analysis series.

The script gets the Beatles songs data: lyrics, year, album, and duration
from free web sources, adds some information and stores the result into the json file
'data.json'.

"""

import json
import requests

from lxml import html
from lxml.etree import tostring


def remove_tags(text):
    """Return text without tags and punctuation marks, stripped"""

    output = text.replace('<br>', ' ').replace('<br/>', ' ')
    output = html.fromstring(output).text_content()
    output = output.replace('\r', '').replace('  ', ' ').strip()
    output = output.replace('...', '')

    characters_to_clean = '.,()[]?!"'

    for character in characters_to_clean:
        output = output.replace(character, '')

    return output


def clean_from_refs(text):
    """Return text without references like [1] in the end of the text"""

    text = text.replace('\r\n', ' ')

    if '[' in text:
        position = text.find('[')
        if position > 0:
            text = text[:position]
    return text


def lowercase(text):
    """Return lowercased string"""

    output = text.lower()
    return output


def normalize_title(title):
    """Return title without ',' and '?'"""
    return title.lower().replace(',', '').replace('?', '')


def is_cover(writers_string):
    """Return True if at least one Beatles member is in the argument iterable"""

    if 'Traditional' in writers_string:
        return True

    for writer in  ('Lennon', 'McCartney', 'Harrison', 'Starkey'):
        if writer in writers_string:
            return False
    return True


def get_formal_writers(writers_string):
    """Return 'Lennon-McCartney' if at least one of them is present in the argument"""

    first_writer = writers_string.split(',')[0]

    if first_writer == 'Starkey':
        return 'Starkey'

    if first_writer == 'Harrison':
        return 'Harrison'

    if 'Lennon' in writers_string or 'McCartney' in writers_string:
        return 'Lennon-McCartney'

    if 'Harrison' in writers_string:
        return 'Harrison'

    if 'Starkey' in writers_string:
        return 'Starkey'

    return writers_string


# titles that are not counted as they are not songs by The Beatles or already present,
# or not songs with lyrics at all
YELLOW_SUBMARINE_TITLES = ('Pepperland', 'Medley: Sea Of Time & Sea Of Holes',
                           'Sea Of Monsters', 'March Of The Meanies',
                           'Pepperland Laid Waste', 'Yellow Submarine In Pepperland',
                           'Yellow Submarine', 'All You Need Is Love')

# German versions of other songs and instrumentals are not counted either
NOT_NEEDED_TITLES = ('Komm, Gib Mir Deine Hand', 'Sie Liebt Dich', 'Flying', 'Revolution 9')

# urls
LYRICS_URL = 'http://www.oldielyrics.com/t/the_beatles.html'
LYRICS_HOST = 'http://www.oldielyrics.com'
WIKI_PAGE = 'https://en.wikipedia.org/wiki/List_of_songs_recorded_by_the_Beatles'

# file to save lyrics data
FILENAME = 'data.json'

# get songs lyrics and albums info

page = requests.get(LYRICS_URL)
tree = html.fromstring(page.content)

# if tere is no data file, get data from web
try:
    with open(FILENAME, 'r') as outfile:
        songs = json.load(outfile)
        print('Collecting songs data from file...')
except:
    songs = []
    print('Collecting songs data from %s...' % LYRICS_URL)

if not songs:

    all_links = tree.cssselect('.album .cap a')
    albums = [link for link in all_links if link.get("itemprop") == "url"]

    last_album_number = len(albums)

    albums = albums[last_album_number-15:last_album_number]

    for album_html in albums:

        album_link = LYRICS_HOST + album_html.get('href')[2:]

        album_page = requests.get(album_link)
        tree = html.fromstring(album_page.content)

        album = {
            'title': tree.cssselect('.album .cap a')[0].text_content(),
            'year': tree.cssselect('.album .cap .flr a')[0].text_content(),
        }


        # Past Masters is a collection of songs from singles, not an album
        if 'Past Masters' in album['title']:
            album['title'] = ''
            album['year'] = ''

        for song_html in tree.cssselect('ol li a'):

            title = song_html.text_content()

            print('Processing song: %s' % title)

            if (album['title'] == 'Yellow Submarine') and (title in YELLOW_SUBMARINE_TITLES):
                continue

            # it's actually two songs
            if title == 'Medley: Kansas City / Hey, Hey, Hey, Hey':
                continue

            if title in NOT_NEEDED_TITLES:
                continue

            # these songs were released both in albums and singles
            released_twice_song = title in ('Love Me Do', 'P.S. I Love You', 'Let It Be',
                                            'Get Back', 'Across The Universe')

            if album['title'] == '' and released_twice_song:
                continue

            song_page = requests.get(LYRICS_HOST + '/' + song_html.get('href')[6:])

            tree = html.fromstring(song_page.content)

            # have to change some titles a bit in order to find them later in Wikipedia
            if title == "When I'm Sixty Four":
                title = "When I'm Sixty-Four"
            elif title == 'Please Mister Postman':
                title = 'Please Mr. Postman'
            elif title == 'You Really Got A Hold On Me':
                title = "You've Really Got A Hold On Me"

            lyrics_verses = tree.cssselect('#lyrics p')
            lyrics_list = [tostring(lyrics_verse).decode("utf-8").strip()
                           for lyrics_verse in lyrics_verses]
            lyrics = '\n'.join(lyrics_list)
            lyrics = lyrics.replace('\n', ' ').replace('\r', '')

            songs.append({
                'title': title,
                'album_title': album['title'],
                'year': album['year'],
                'lyrics': lyrics,
                'cleaned_lyrics': remove_tags(lyrics)
                })

    with open(FILENAME, 'w') as outfile:
        json.dump(songs, outfile)


print('Done.')
print('Collecting songs data from wikipedia...')

# get songs length from wikipedia

all_songs_tree = html.fromstring(requests.get(WIKI_PAGE).content)

all_songs_tree_table = all_songs_tree.cssselect('table.wikitable')[1].cssselect('tr')

song_titles_and_numbers = {normalize_title(song['title']): number
                           for number, song in enumerate(songs)}

for item_tr in all_songs_tree_table:

    item_td = item_tr[0].cssselect('th a')

    if not item_td:
        continue

    item = item_td[0].text_content()

    if normalize_title(item) in song_titles_and_numbers.keys():

        song = songs[song_titles_and_numbers[normalize_title(item)]]

        if not song['year']:
            year = item_tr[4].cssselect('td')
            if year:
                song['year'] = year[0].text_content()

        writers = item_tr[2].cssselect('td')

        if writers:
            song['writers'] = clean_from_refs(writers[0].text_content())

        vocals = item_tr[3].cssselect('td')

        if vocals:
            song['vocals'] = clean_from_refs(vocals[0].text_content())


        song_link = item_td[0].get('href')
        song_page = requests.get('https://en.wikipedia.org%s' % song_link, allow_redirects=True)
        tree = html.fromstring(song_page.content)
        info_item = tree.cssselect('table.infobox td.plainlist span.duration')[0]
        minutes = int(info_item.cssselect('span.min')[0].text_content())
        seconds = int(info_item.cssselect('span.s')[0].text_content())
        song['length'] = minutes*60 + seconds

for song in songs:

    song['num_words_in_title'] = len(song['title'].split(' '))
    song['num_words_in_lyrics'] = len(song['cleaned_lyrics'].split(' '))
    song['lowercase_lyrics'] = lowercase(song['cleaned_lyrics'])

    song['cover'] = is_cover(song['writers'])
    song['formal_writers'] = get_formal_writers(song['writers'])

    if 'length' not in song or song['year'] == '':
        print('Problem!', song['title'], song['album_title'])

print('Done.')

print('Writing data to file...')

with open(FILENAME, 'w') as outfile:
    json.dump(songs, outfile)

print('The end.')
