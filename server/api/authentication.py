
from tastypie.authentication import Authentication, ApiKeyAuthentication


class OriginAuthentication(ApiKeyAuthentication):
    def is_authenticated(self, request, **kwargs):
        if request.method == 'GET':
            return super(OriginAuthentication, self).is_authenticated(self, request, **kwargs)
        elif request.method == 'POST':
            return super(OriginAuthentication, self).is_authenticated(self, request, **kwargs)
        elif request.method == 'PUT':
            return False
        elif request.method == 'DELETE':
            return False
        else:
            return False
    
