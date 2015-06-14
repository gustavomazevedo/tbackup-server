#-*- coding: utf-8 -*-

from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import FieldError
from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse

from rest_framework import viewsets, status, permissions, parsers, mixins
from rest_framework.response import Response

from .models import Backup
from .models.destination.BaseDestination import BaseDestination

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
