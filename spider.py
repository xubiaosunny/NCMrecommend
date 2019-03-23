import sys, os
import django
import time
import logging


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([BASE_DIR, ])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NCMrecommend.settings')
django.setup()

import requests
from api.models import *

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=os.path.join(BASE_DIR, 'spider.log'), level=logging.INFO, format=LOG_FORMAT)

PROXY_HOST = 'http://localhost:3000'


def get_tag():
    rep = requests.get(PROXY_HOST + '/playlist/catlist')
    data = rep.json()

    for tag in data['sub']:
        if Tag.objects.filter(name=tag['name']).exists():
            Tag.objects.filter(name=tag['name']).update(category=tag['category'])
        else:
            Tag.objects.create(name=tag['name'], category=tag['category'])


def get_music_from_playlist(p):
    start_time = time.time()
    rep = requests.get(PROXY_HOST + '/playlist/detail?id=%d' % p)
    data = rep.json()
    if str(data['code']) == '200':
        playlist = data['playlist']
        if len(playlist['tracks']) <= 1:
            logging.info('Your ip may have been blocked!!!')
            exit(0)
        tags = Tag.objects.filter(name__in=playlist['tags'])
        if PlayList.objects.filter(p_id=playlist['id']).exists():
            pl = PlayList.objects.get(p_id=playlist['id'])
            # pl.name = playlist['name']
            # pl.save()
            o_tags = pl.tags.all()
            o_diff_tags = o_tags.exclude(pk__in=tags)
            diff_tags = tags.exclude(pk__in=o_tags)
            if o_diff_tags:
                pl.tags.remove(*o_diff_tags)
            if diff_tags:
                pl.tags.add(*diff_tags)
        else:
            pl = PlayList.objects.create(name=playlist['name'], p_id=playlist['id'])
            pl.tags.add(*tags)

        for track in playlist['tracks']:
            if Music.objects.filter(m_id=track['id']).exists():
                music = Music.objects.get(m_id=track['id'])
                # music.name=track['name']
                # music.save()
                if not music.playlists.filter(pk=pl.pk).exists():
                    music.playlists.add(pl)
            else:
                music = Music.objects.create(name=track['name'], m_id=track['id'])
                music.playlists.add(pl)
    else:
        logging.info("%d: %s" % (p, data['msg']))

    end_time = time.time()
    sleep_time = 10 - int(end_time - start_time)
    sleep_time = sleep_time if sleep_time > 0 else 0
    time.sleep(sleep_time)


def get_music_from_hot_playlist():
    p_file = os.path.join(BASE_DIR, 'hot_process.txt')
    p = 0
    if os.path.exists(p_file):
        with open(p_file) as f:
            p = int(f.read())
    else:
        with open(p_file, 'w') as f:
            f.write(str(p))

    tags = Tag.objects.all().order_by('id')[p:]
    for i, tag in enumerate(tags):
        rep = requests.get(PROXY_HOST + '/top/playlist?limit=1000&order=hot&cat=%s' % tag.name)
        for j, pl in enumerate(rep.json()['playlists']):
            logging.info("Tag %s index %d playlist %d: start" % (tag.name, j, pl['id'],))
            get_music_from_playlist(pl['id'])

        with open(p_file, 'w') as f:
            f.write(str(p + i))



def get_music_from_default_playlist():
    p_file = os.path.join(BASE_DIR, 'process.txt')
    p = 0
    if os.path.exists(p_file):
        with open(p_file) as f:
            p = int(f.read())
    else:
        with open(p_file, 'w') as f:
            f.write(str(p))

    while True:
        p += 1
        logging.info("playlist %d: start" % (p,))
        get_music_from_playlist(p)
        #
        with open(p_file, 'w') as f:
            f.write(str(p))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        logging.info('spider.py [ tag | music_from_default_playlist | music_from_hot_playlist ]')
        exit(0)

    if sys.argv[1] == 'tag':
        get_tag()
    elif sys.argv[1] == 'music_from_default_playlist':
        get_music_from_default_playlist()
    elif sys.argv[1] == 'music_from_hot_playlist':
        get_music_from_hot_playlist()
    else:
        logging.info('spider.py [ tag | music_from_default_playlist | music_from_hot_playlist ]')
