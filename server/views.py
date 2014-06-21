#-*- coding: utf-8 -*-
import json
import operator

from datetime import datetime

from Crypto.Hash import SHA

from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import Backup, Origin
from .models.destination.BaseDestination import BaseDestination


#@require_POST
@csrf_exempt
def register_origin(request):
    #import ipdb; ipdb.set_trace()
    if request.method == "POST":
        if not authenticated(None, request.POST.dict()):
            return HttpResponseForbidden()
        oname = request.POST.get(u"origin", None)
        print oname
        if not oname:
            return HttpResponseBadRequest(u"<h1>valor inválido</h1>")
        
        origin, created = Origin.objects.get_or_create(
            name=oname
        )
        print origin, created
        if not created:
            return HttpResponseBadRequest(u"<h1>Origem já está cadastrada</h1>")
        
        return json_response(
            get_signed_data(
                {u"origin": origin.name,
                 u"id"    : origin.id,
                 u"apikey": unicode(origin.apikey),
                },
                settings.R_SIGNATURE_KEY
            )
        )
    else:
        return HttpResponseNotFound(u"<h1>Não há nada aqui @_@</h1>")


@require_GET
def retrieve_destinations(request, id):
    #if request.method == 'GET':
        if not id or not authenticated(id, request.GET.dict()):
            return HttpResponseForbidden()
        
        return json_response(
            get_signed_data(
                {u"destinations": [d.name for d in BaseDestination.objects.all()]},
                Origin.objects.get(id=id).apikey
            )
        )
    #else:
    #    return HttpResponseNotFound()

def authenticated(id, fulldata):
    signature = fulldata.get(u"signature", None)
    data = remove_key(fulldata, u"signature")
    #import ipdb; ipdb.set_trace()
    if not signature:
        return False
    try:
        return signature == sign(data, Origin.objects.get(id=id).apikey)
    except Origin.DoesNotExist:
        if id:
            return False
        return signature == sign(data, settings.R_SIGNATURE_KEY)
    
def sign(data, key):
    sha1 = SHA.new()
    if not data:
        sha1.update(u"None")
    else:
        sorted_data = sorted(data.iteritems(),key=operator.itemgetter(0))
        for item in sorted_data:
            sha1.update(unicode(item))
    sha1.update(key)
    
    import ipdb; ipdb.set_trace()
    return sha1.hexdigest()

def get_signed_data(data, key):
    return_data = dict(data) if data else {}
    #import ipdb; ipdb.set_trace()
    return_data[u"timestamp"] = u"%s" % json.dumps(unicode(datetime.now()))
    return_data[u"signature"] = u"%s" % sign(return_data, key)
    #import ipdb; ipdb.set_trace()
    return return_data

def remove_key(d, key):
    r = dict(d)
    del r[key]
    return r

#@require_POST
@csrf_exempt
def backup(request, id):
    if request.method == 'POST':
        #return json_response([request.POST, request.FILES])
        #values = request.POST.get('values', None)
        #if not values:
        #    print u'<h1>valor inválido</h1>'
        #    return HttpResponseBadRequest(u'<h1>valor inválido</h1>')
        
        django_file = request.FILES.get('file', None)
        if not django_file:
            print u'<h1>nenhum arquivo recebido</h1>'
            return HttpResponseBadRequest(u'<h1>nenhum arquivo recebido</h1>')
        
        #if values['sha1sum'] != file_sha_checksum(django_file):
        #    print u'<h1>arquivo corrompido</h1>'
        #    return HttpResponseBadRequest(u'<h1>arquivo corrompido</h1>')
        
        to_bool = lambda b: bool(b) and b.lower() not in ('false', '0')
        return json_response(
            backup_file(
                django_file,
                request.POST.get('origin', None),#values['origin'],
                request.POST.get('destination', None),#values['destination'],
                request.POST.get('date', None), #values['date'],
                request.POST.get('sha1sum', None),#None, #values['sha1sum'],
                to_bool(request.POST.get('before_restore', None)),#values['before_restore'],
                to_bool(request.POST.get('after_restore', None)),#values['after_restore'],
            )
        )
    else:
        print u'<h1>não há nada aqui @_@</h1>'
        return HttpResponseNotFound(u'<h1>não há nada aqui @_@</h1>')

#@require_POST
@csrf_exempt
def restore(request, id):
    return HttpResponseNotFound(u'<h1>não implementado</h1>')
    #if request.method == 'GET':
    #    return HttpResponse(
    #        json.dumps(
    #            restore_file(
    #                request.GET
    #            )
    #        )
    #    )
    #else:
    #    return HttpResponseNotFound()

@csrf_exempt
def message(request, id):
    pass

def json_response(data):
    return HttpResponse(
        json.dumps(data),
        content_type='application/json; charset=utf-8'
    )


def file_sha_checksum(django_file):
    sha1 = SHA.new()
    for chunk in django_file.chunks():
        sha1.update(chunk)
    return sha1.hexdigest()

def backup_file(django_file, from_origin, to_destination,
                date, sha1sum, before_restore, after_restore):
    o = Origin.objects.get(name=from_origin)
    d = BaseDestination.objects.get(name=to_destination)
    b = Backup.objects.create(
        name=django_file.name,
        origin=o,
        destination=d,
        date=date,
    )
    try:
        r = b.backup(django_file, before_restore, after_restore)
        if r:
            return r
        else:
            b.delete()
            return r
    except:
        b.delete()
        return False
        
