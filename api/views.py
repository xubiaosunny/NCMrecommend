from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
import json
import copy
import math
from api.models import HistoryRecord, Music,PlayList
# Create your views here.


def render_success(data):
    return HttpResponse(json.dumps({'code': 200, 'data': data}), content_type="text/json", status=200)


def render_fail(msg, code=400):
    return HttpResponse(json.dumps({'code': code, 'msg': msg}), content_type="text/json", status=200)


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


def get_recommend(request):
    u_id = request.GET.get('u_id')
    if not u_id:
        return render_fail('require u_id')
    limit = int(request.GET.get('limit', 10))
    records = HistoryRecord.objects.filter(u_id=u_id).order_by('-id')[:50]
    h_musices = Music.objects.filter(m_id__in=[r.m_id for r in records])

    tag_num_dict = {}
    total_sum = 0
    print([p.name for p in Music.objects.get(pk=1).playlists.all()])
    for m in h_musices:
        print(m.name)
        for pl in m.playlists.all():
            print('--', pl.name)
            for tag in pl.tags.all():
                print('  --', tag.name)
                if tag.name in tag_num_dict:
                    tag_num_dict[tag.name] += 1
                else:
                    tag_num_dict[tag.name] = 1
                total_sum += 1
    recommend = []
    print(tag_num_dict)
    for tag, num in copy.deepcopy(tag_num_dict).items():
        count = math.ceil((num / total_sum) * limit)

    return render_success({})

    