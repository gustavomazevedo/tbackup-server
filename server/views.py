#-*- coding: utf-8 -*-
import json
import operator

import StringIO

from datetime import datetime

from Crypto.Hash import SHA

from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
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
        return HttpResponseForbidden()
    elif not authenticated(id, request.GET.dict()):
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
from django.core.servers.basehttp import FileWrapper
from rest_framework import viewsets, views, status, permissions, parsers, mixins, filters
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
        q = request.GET
        q_type = q.get('query_type', None)
        
        #if AnonymousUser or logged in user with param query_type=availability,
        #determines if username is available
        if isinstance(user, AnonymousUser) or (q_type is not None and q_type == 'availability'):
            q_username = q.get('username', None)
            if q_username is None:
                return Response({'error': 'No username specified'})
            
            if User.objects.filter(username=q_username).exists():
                return Response({'available': False})
            
            return Response({'available': True})        
        
        return super(UserViewSet, self).list(request)
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()
        user = request.user
        if not user.is_superuser and not user.is_staff and self.object and self.object != request.user:
            return Response({'error': 'You are not authorized to run this action'},
                            status=status.HTTP_403_FORBIDDEN)
        return super(UserViewSet, self).update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()
        user = request.user
        if not user.is_superuser and not user.is_staff and self.object and self.object != request.user:
            return Response({'error': 'You are not authorized to run this action'},
                            status=status.HTTP_403_FORBIDDEN)
        return super(UserViewSet, self).patch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        username = self.kwargs.get('username', self.request.QUERY_PARAMS.get('username', None))
            
        #if admin
        if user.is_superuser:
            if username is not None:
                #filters by username
                return User.objects.filter(username=username)
            else:
                #does not filter
                return User.objects.all()
        
        #else, only allow regular user to filter its own name
        if not username or username == user.username:
            #filters own name
            return User.objects.filter(username=user)
        else:
            #empty result
            return []
    
    

class PrivateModelMixin(object):
    permission_class = permissions.DjangoModelPermissionsOrAnonReadOnly
    
    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return []
        elif user.is_superuser:
            return super(PrivateModelMixin, self).get_queryset()
        else:
            qs = super(PrivateModelMixin, self).get_queryset()
            try:
                return qs.filter(user__id=user.id)
            except FieldError:
                return qs
    
class DestinationViewSet(PrivateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = BaseDestination.objects.all()
    serializer_class = DestinationSerializer


class IsOwnerOrSuperuser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.user == request.user
        
    

class BackupViewSet(PrivateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    parser_classes = (parsers.MultiPartParser,parsers.FormParser)
    queryset = Backup.objects.all()
    serializer_class = BackupSerializer
    permission_classes = (IsOwnerOrSuperuser,)
    
    def retrieve(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.file_as_download(request)
        if response:
            return response
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        if self.object_list.count() == 1:
            self.object = self.object_list[0]
            response = self.file_as_download(request)
            if response:
                return response
        return super(BackupViewSet, self).list(request, *args, **kwargs)
    
    def file_as_download(self, request):
        fileformat = request.GET.get('fileformat', None)
        if fileformat == 'raw':
            #if offline file is available
            if self.object.file:
                f = self.object.file
            #else try to restore from destination
            else:
                try:
                    f = self.object.restore()
                except Exception, e:
                    raise
            if f:
                file_response = StreamingHttpResponse(FileWrapper(f), content_type='application/zip')
                file_response['Content-Disposition'] = 'attachment; filename="%s"' % self.object.name
                return file_response
        return None
    
    def get_queryset(self):
        fields = (
            ('name', 'name__contains'),
            ('destination','destination__name__contains'),
            ('date', 'date'),
            ('min_date', 'date__gte'),
            ('max_date', 'date__lte')
        )
        
        query = { datafield : self.request.GET[reqfield]
                  for reqfield, datafield in fields
                  if self.request.GET.get(reqfield, None)
                }
        
        if not self.request.user.is_superuser:
            query.update({'user': self.request.user})
            
        return Backup.objects.filter(**query)
