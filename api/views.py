from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
import json
import copy
import math
import random
from api.models import HistoryRecord, Music, Tag, MusicCollection
# Create your views here.


def render_success(data):
    response = HttpResponse(json.dumps({'code': 200, 'data': data}), content_type="text/json", status=200)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def render_fail(msg, code=400):
    response = HttpResponse(json.dumps({'code': code, 'msg': msg}), content_type="text/json", status=200)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def set_record(request):
    u_id = request.JSON.get('u_id')
    if not u_id:
        return render_fail('require u_id')
    m_id = request.JSON.get('m_id')
    if not m_id:
        return render_fail('require m_id')
    m_name = request.JSON.get('m_name')
    r = HistoryRecord.objects.create(u_id=u_id, m_id=m_id, m_name=m_name)
    return render_success(
        {'u_id': r.u_id, 'm_id': r.m_id, 'm_name': r.m_name,
         'time': timezone.localtime(r.time).strftime('%Y-%m-%d %H:%M:%S') })


def get_record(request):
    u_id = request.GET.get('u_id')
    if not u_id:
        return render_fail('require u_id')
    limit = int(request.GET.get('limit', 10))
    records = HistoryRecord.objects.filter(u_id=u_id).order_by('-id')[:limit]
    data = [{'m_id': r.m_id, 'm_name': r.m_name, 'time': timezone.localtime(r.time).strftime('%Y-%m-%d %H:%M:%S')}
            for r in records]
    return render_success(data)


def add_music_collection(request):
    u_id = request.JSON.get('u_id')
    if not u_id:
        return render_fail('require u_id')
    m_id = request.JSON.get('m_id')
    if not m_id:
        return render_fail('require m_id')
    m_name = request.JSON.get('m_name')
    if MusicCollection.objects.filter(u_id=u_id, m_id=m_id).exists():
        return render_fail('already exist')
    r = MusicCollection.objects.create(u_id=u_id, m_id=m_id, m_name=m_name)
    return render_success(
        {'u_id': r.u_id, 'm_id': r.m_id, 'm_name': r.m_name,
         'time': timezone.localtime(r.time).strftime('%Y-%m-%d %H:%M:%S') })



def del_music_collection(request):
    u_id = request.JSON.get('u_id')
    if not u_id:
        return render_fail('require u_id')
    m_id = request.JSON.get('m_id')
    if not m_id:
        return render_fail('require m_id')
    try:
        collection = MusicCollection.objects.get(u_id=u_id, m_id=m_id)
    except:
        return render_fail('not exist')
    collection.delete()
    return render_success({'u_id': u_id, 'm_id': m_id })


def get_music_collection(request):
    u_id = request.GET.get('u_id')
    if not u_id:
        return render_fail('require u_id')
    records = MusicCollection.objects.filter(u_id=u_id).order_by('-id')
    data = [{'m_id': r.m_id, 'm_name': r.m_name, 'time': timezone.localtime(r.time).strftime('%Y-%m-%d %H:%M:%S')}
            for r in records]
    return render_success(data)


def get_recommend(request):
    u_id = request.GET.get('u_id')
    limit = int(request.GET.get('limit', 10))
    ret = []
    if u_id:
        records = HistoryRecord.objects.filter(u_id=u_id).order_by('-id')[:50]
        h_musices = Music.objects.filter(m_id__in=[r.m_id for r in records])

        tag_num_dict = {}
        total_sum = 0
        for m in h_musices:
            # print('-', m.name)
            for pl in m.playlists.all():
                # print('  --', pl.name)
                for tag in pl.tags.all():
                    # print('    ---', tag.name)
                    if tag.name in tag_num_dict:
                        tag_num_dict[tag.name] += 1
                    else:
                        tag_num_dict[tag.name] = 1
                    total_sum += 1

        collections = MusicCollection.objects.filter(u_id=u_id)
        c_musices = Music.objects.filter(m_id__in=[r.m_id for r in collections])
        # collection double ratio
        for m in c_musices:
            # print('-', m.name)
            for pl in m.playlists.all():
                # print('  --', pl.name)
                for tag in pl.tags.all():
                    # print('    ---', tag.name)
                    if tag.name in tag_num_dict:
                        tag_num_dict[tag.name] += 2
                    else:
                        tag_num_dict[tag.name] = 2
                    total_sum += 2

        for tag, num in copy.deepcopy(tag_num_dict).items():
            count = math.ceil((num / total_sum) * limit)
            playlists = Tag.objects.get(name=tag).playlist_set.all()

            for i in random.sample(range(playlists.count()), count):
                sample_music = playlists[i].music_set.order_by('?').first()
                ret.append({
                    'm_id': sample_music.m_id,
                    'name': sample_music.name,
                    'tag': tag,
                })
    else:
        musices = Music.objects.all()
        for i in random.sample(range(musices.count()), limit):
            sample_music = musices[i]
            ret.append({
                'm_id': sample_music.m_id,
                'name': sample_music.name,
            })
    random.shuffle(ret)
    return render_success(ret[:limit])
