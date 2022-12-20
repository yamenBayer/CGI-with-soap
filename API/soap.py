from django.views.decorators.csrf import csrf_exempt
from spyne.application import Application
from spyne.decorator import rpc
from spyne.model.primitive import Boolean,Unicode, Integer, Double, String, DateTime 
from spyne.protocol.soap import Soap11
from spyne.protocol.xml import XmlDocument
from spyne.protocol.http import HttpRpc
from spyne.server.django import DjangoApplication
from spyne.service import ServiceBase
import json
from spyne import Iterable, Array, ComplexModel
from django.forms.models import model_to_dict
from django.db import IntegrityError
from spyne.error import ResourceNotFoundError
from spyne.model.fault import Fault
from django.db.models.deletion import ProtectedError
from API import face_recognition

from API.views import getNamesList
from .models import *

globalpath = None
class C_Services(ComplexModel):
    id = Integer
    name = String
    type = String
    api_key = String
    status = Boolean
    socket_ip = String
    live_type = Boolean

class C_FC(ComplexModel):
    id = Integer
    name = String
    created_at = DateTime
    api_key = String

class SoapService(ServiceBase):
    

    @rpc(Unicode , Integer, _returns=Array(C_Services))
    def get_service(ctx, api_key, pid):
        profile = Profile.objects.get(id = pid)
        service = Services.objects.filter(owner = profile, api_key = api_key).values('id','name','type','api_key','status','socket_ip','live_type')
        if not service.exists():
            raise
        return service

    @rpc(Integer ,_returns=Array(C_Services))
    def get_services(ctx, pid):
        profile = Profile.objects.get(id = pid)
        services = Services.objects.filter(owner = profile).values('id','name','type','api_key','status','socket_ip','live_type')
        if not services.exists():
            raise
        return services

    @rpc(Integer, Integer ,_returns=Array(C_FC))
    def get_face(ctx, id, pid):
        profile = Profile.objects.get(id = pid)
        face = Face_Collection.objects.filter(id = id, owner = profile).values('id', 'name','created_at','api_key')
        if not face.exists():
            raise
        return face

    @rpc(Integer ,_returns=Array(C_FC))
    def get_faces(ctx, pid):
        profile = Profile.objects.get(id = pid)
        faces = Face_Collection.objects.filter(owner = profile).values('id', 'name','created_at','api_key')
        if not faces.exists():
            raise
        return faces

    @rpc(Unicode , Integer ,_returns=Array(C_FC))
    def get_service_faces(ctx, api_key, pid):
        profile = Profile.objects.get(id = pid)
        faces = Face_Collection.objects.filter(owner = profile, api_key = api_key).values('id', 'name','created_at','api_key')
        if not faces.exists():
            raise
        return faces

    @rpc(Unicode ,Integer, String ,_returns=Array(C_FC))
    def video_test(ctx, api_key, pid, path):
        profile = Profile.objects.get(id = pid)
        service = Services.objects.get(api_key = api_key)
        people = Person.objects.filter()
        count = people.count() - 1
        names = getNamesList(people)
        queryset = face_recognition.video_recognize(service.api_key, profile,path,count,names)
        if not queryset:
            return None
        test = 'CGI'
        response = Face_Collection.objects.none()
        for item in queryset:
            if type(item) == type(test):
                global globalpath
                globalpath = item
            else:
                response |= Face_Collection.objects.filter(id=item).values('id', 'name','created_at','api_key')
        return response

    @rpc(_returns=String)
    def get_path(ctx):
        return globalpath

application = Application([SoapService],
    tns='django.soap.example',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

def INIT():
    django_app = DjangoApplication(application)
    app = csrf_exempt(django_app)

    return app
