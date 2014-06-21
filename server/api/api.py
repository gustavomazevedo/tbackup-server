# -*- coding: utf-8 -*-

from tastypie.api import Api
from .v1.resources import (
    OriginResource,
    DestinationResource,
    BackupResource,
    RecoverResource
    )

v1_api = Api(api_name='v1')
v1_api.register(OriginResource())
v1_api.register(DestinationResource())
v1_api.register(BackupResource())
v1_api.register(RecoverResource())

