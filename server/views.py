#-*- coding: utf-8 -*-
import json
import operator

import StringIO

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


@require_GET
def origin_available(request):
    if not authenticated(None, request.GET.dict()):
        return HttpResponseForbidden()
    origin_name = request.GET.get(u"origin", None)
    if not origin_name:
        return HttpResponseBadRequest(u"<h1>valor inválido</h1>")

    respond = lambda available: json_response({u"availability":available})
    origin = Origin.objects.filter(name=origin_name)
    return respond(False) if origin.exists() else respond(True)
    
@require_POST
@csrf_exempt
def register_origin(request):
    #import ipdb; ipdb.set_trace()
    #if request.method == "POST":
    if not authenticated(None, request.POST.dict()):
        return HttpResponseForbidden()
    origin_name = request.POST.get(u"origin", None)
    if not origin_name: return HttpResponseBadRequest(u"<h1>valor inválido</h1>")
    
    origin = Origin.objects.create(name=origin_name)
    return json_response({ u"origin": origin.name,
                           u"id"    : origin.id,
                           u"apikey": unicode(origin.apikey)
                         })
    #else:
    #    return HttpResponseNotFound(u"<h1>Não há nada aqui @_@</h1>")


@require_GET
def retrieve_destinations(request, id):
    return return_or_error(request, id, lambda: json_response(
        {u"destinations": [d.name for d in BaseDestination.objects.all()]},
        Origin.objects.get(id=id).apikey ))

def return_or_error(request, id, action):
    error = get_authentication_error(request, id)    
    return error if error else action()

def get_authentication_error(request, id):
    if not id:
        #import ipdb; ipdb.set_trace()
        print 'not id'
        return HttpResponseForbidden()
    elif not authenticated(id, request.GET.dict()):
        print 'not authenticated'
        #import ipdb; ipdb.set_trace()
        return HttpResponseForbidden()
    return None

def authenticated(id, fulldata):
    signature = fulldata.get(u"signature", None)
    data = remove_key(fulldata, u"signature")
    origin = Origin.objects.filter(id=id)
    apikey = origin[0].apikey if origin.exists() else None
    #import ipdb; ipdb.set_trace()
    return False if not signature else signature == sign(data, apikey)
    
def sign(data, apikey=None):
    sha1 = SHA.new()
    if not data:
        sha1.update(u"None")
    else:
        sorted_data = sorted(data.iteritems(),key=operator.itemgetter(0))
        for item in sorted_data:
            sha1.update(unicode(item))
    used_key = apikey or settings.R_SIGNATURE_KEY
    sha1.update(used_key)
    #import ipdb; ipdb.set_trace()
    return sha1.hexdigest()

def get_signed_data(data, apikey):
    return_data = dict(data) if data else {}
    return_data[u"timestamp"] = u"%s" % json.dumps(unicode(datetime.now()))
    return_data[u"signature"] = u"%s" % sign(return_data, apikey)
    #import ipdb; ipdb.set_trace()
    return return_data

def remove_key(d, key):
    r = dict(d)
    del r[key]
    return r

@require_POST
@csrf_exempt
def backup(request, id):
    error = get_authentication_error(request, id)
    if error:
        return error
    
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
            request.POST.get('origin', None),
            request.POST.get('destination', None),
            request.POST.get('date', None),
            request.POST.get('sha1sum', None),
            to_bool(request.POST.get('before_restore', None)),
            to_bool(request.POST.get('after_restore', None)),
        )
    )
    
#@require_POST
@csrf_exempt
def restore(request, id):
    error = get_authentication_error(request, id)
    if error:
        return error
    
    o = Origin.objects.get(name=request.POST.get('origin', None))
    d = BaseDestination.objects.get(name=request.POST.get('destination', None))
    filename = request.POST.get('filename', None)
    b = Backup.objects.get(name=filename,
                              origin=o,
                              destination=d,
                              date=request.POST.get('date', None))
    o = Origin.objects.get(name=request.GET.get('origin', None))
    d = BaseDestination.objects.get(name=request.GET.get('destination', None))
    filename = request.GET.get('filename', None)
    b = Backup.objects.get(name=filename,
                              origin=o,
                              destination=d,
                              date=request.GET.get('date', None))
    f = StringIO.StringIO()
    chunks, success = b.restore()
    if success:
        for chunk in chunks:
            f.write(chunk)
    
    response = HttpResponse(FileWrapper(f.getvalue()), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response['Content-Length'] = f.tell()
    
    return response
    
    #return HttpResponseNotFound(u'<h1>não implementado</h1>')

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

def json_response(data, apikey=None):
    return HttpResponse( json.dumps(get_signed_data(data, apikey)),
                         content_type='application/json; charset=utf-8' )


def file_sha_checksum(django_file):
    sha1 = SHA.new()
    for chunk in django_file.chunks():
        sha1.update(chunk)
    return sha1.hexdigest()

def backup_file(django_file, from_origin, to_destination,
                date, sha1sum, before_restore, after_restore):
    o = Origin.objects.get(name=from_origin)
    d = BaseDestination.objects.get(name=to_destination)
    b = Backup.objects.create(name=django_file.name,
                              origin=o,
                              destination=d,
                              date=date)
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
        

from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import FieldError
from rest_framework import viewsets, views, status, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from .serializers import UserSerializer, DestinationSerializer, BackupSerializer

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_class = permissions.IsAuthenticatedOrReadOnly
    
    def list(self, request):
        user = request.user
        q = request.QUERY_PARAMS
        q_type = q.get('query_type', None)
        
        #if AnonymousUser or logged in user with param query_type=availability,
        #determines if username is available
        if isinstance(user, AnonymousUser) or (q_type is not None and q_type == 'availability'):
            q_username = request.QUERY_PARAMS.get('username', None)
            if q_username is None:
                return Response({'error': 'No username specified'})
            
            if User.objects.filter(username=q_username).exists():
                return Response({'available': False})
            
            return Response({'available': True})        
        
        return super(UserViewSet, self).list(request)
    
    @detail_route(methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.DATA)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        
    def get_queryset(self):
        
        #filters by kwargs or QUERY_PARAMS
        username = self.kwargs.get('username', self.request.QUERY_PARAMS.get('username', None))
        if username is not None:
            return User.objects.filter(username=username)
        
        #if admin, no filter applied
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        #filter current user
        return User.objects.filter(username=user)

class PrivateModelViewSet(viewsets.ModelViewSet):
    permission_class = permissions.IsAuthenticatedOrReadOnly
    
    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return []
        elif user.is_superuser:
            return super(PrivateModelViewSet, self).get_queryset()
        else:
            qs = super(PrivateModelViewSet, self).get_queryset()
            print qs
            try:
                return qs.filter(user__id=user.id)
            except FieldError:
                try:
                    return qs.filter(users__id=user.id)
                except FieldError:
                    return qs
    
class DestinationViewSet(PrivateModelViewSet):
    queryset = BaseDestination.objects.all()
    serializer_class = DestinationSerializer
    
class BackupViewSet(PrivateModelViewSet):
    queryset = Backup.objects.all()
    serializer_class = BackupSerializer
    
    
#
#class UserAvailableView(generics.ListAPIView):
#    serializer_class = UserSerializer
#    
#    def get_queryset(self, request, *args, **kwargs):
#        username = request.DATA.get('username', None)
#        
#        if username:
#            queryset = queryset.filter(username=username)
#            
#        return queryset
#    
#    def get(self, request, *args, **kwargs):
#        return Response({'available': })