from desk.model import Desk
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
#from rest_framework.viewsets import ViewSet
from desk.forms import DeskModelForm
from desk.mixins import HttpResponseMixin
from user_auth.models import CustomGroup


class DeskDetailApiView(APIView, HttpResponseMixin):
    """
    View for just one object instance
    """

    is_json = True
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, *args, **kwargs):
        obj = Desk.objects.get(id=id)
        json_data = obj.serialize()

        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        json_data = json.dumps({"Message": "use api_desks/desks/ endpoint in order to create Desk"})
        return self.render_to_response(json_data, 403)

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class DeskModelListApiView(APIView, HttpResponseMixin):
    """
    post:
    Create a new Desk instance
    """
    is_json = True
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, *args, **kwargs):
        qs = Desk.objects.all()
        json_data = qs.serialize()

        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):

        form = DeskModelForm(request.POST)
        if form.is_valid():
            obj = Desk.objects.create(author=request.user, name=request.POST["name"],
                                      description=request.POST["description"])

            basic_group = CustomGroup.objects.create(name="POOL_" + obj.name + "_" + str(obj.id),
                                                     related_desk=obj)
            obj.save()
            obj_data = obj.serialize()
            return self.render_to_response(obj_data)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, 400)
        data = {'error': 'Not Allowed'}
        return self.render_to_response(data, 403)
