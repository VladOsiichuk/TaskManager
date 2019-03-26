from desk.model import Desk
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
#from rest_framework.viewsets import ViewSet
from desk.forms import DeskModelForm
from desk.mixins import HttpResponseMixin
from user_auth.models import CustomGroup
from rest_framework import viewsets
from .serializers import DeskSerializer


class DeskDetailApiView(viewsets.ViewSet, HttpResponseMixin, viewsets.GenericViewSet):
    """
    create:
    Create new instance
    """

    is_json = True
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = DeskSerializer

    def retrieve(self, request, pk):
        try:
            obj = Desk.objects.get(id=pk)
            json_data = obj.serialize()
            return self.render_to_response(json_data)

        except Desk.DoesNotExist:
            json_data = json.dumps({"message": "Desk with your id does not exists"})
            return self.render_to_response(json_data, 404)

    def create(self, request, *args, **kwargs):
        json_data = json.dumps({"Message": "use api_desks/desks/ endpoint in order to create Desk"})
        return self.render_to_response(json_data, 403)

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


class DeskModelListApiView(viewsets.ViewSet, HttpResponseMixin):
    """
    post:
    Create a new Desk instance
    """
    is_json = True
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def list(self, request, *args, **kwargs):
        qs = Desk.objects.all()
        json_data = qs.serialize()

        return self.render_to_response(json_data)

    def create(self, request, *args, **kwargs):

        form = DeskModelForm(request.POST)
        if form.is_valid():
            obj = Desk.objects.create(author=request.user, name=request.POST["name"],
                                      description=request.POST["description"])

            basic_group = CustomGroup.objects.create(name="POOL_" + obj.name + "_" + str(obj.id),
                                                     related_desk=obj)

            editor_group = CustomGroup.objects.create(name="EDITOR_" + obj.name + "_" + str(obj.id),
                                                      related_desk=obj)

            staff_group = CustomGroup.objects.create(name="STAFF_" + obj.name + "_" + str(obj.id),
                                                     related_desk=obj)
            basic_group.save()
            editor_group.save()
            staff_group.save()
            obj.save()
            obj_data = obj.serialize()
            return self.render_to_response(obj_data)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, 400)
        data = {'error': 'Not Allowed'}
        return self.render_to_response(data, 403)
