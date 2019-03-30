from desk.model import Desk
from .serializers import DeskSerializer
from rest_framework import generics
from rest_framework import mixins, permissions
from rest_framework.authentication import SessionAuthentication
import json
from api_rules.models import PermissionRow
from user_auth.models import UsersDesks, CustomGroup
from rest_framework import status
from rest_framework.response import Response
from api_rules.permissions import IsAdminOfDesk, IsEditorOfDeskOrHigher


# class DeskDetailApiView(viewsets.ViewSet, HttpResponseMixin, viewsets.GenericViewSet):
#     """
#     create:
#     Create new instance
#     """
#
#     is_json = True
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
#     permission_classes = (IsAuthenticated,)
#
#     serializer_class = DeskSerializer
#
#     def retrieve(self, request, pk):
#         try:
#             obj = Desk.objects.get(id=pk)
#             json_data = obj.serialize()
#             return self.render_to_response(json_data)
#
#         except Desk.DoesNotExist:
#             json_data = json.dumps({"message": "Desk with your id does not exists"})
#             return self.render_to_response(json_data, 404)
#
#     def create(self, request, *args, **kwargs):
#         json_data = json.dumps({"Message": "use api_desks/desks/ endpoint in order to create Desk"})
#         return self.render_to_response(json_data, 403)
#
#     def update(self, request, *args, **kwargs):
#         pass
#
#     def destroy(self, request, *args, **kwargs):
#         pass


# class DeskModelListApiView(viewsets.ViewSet, HttpResponseMixin):
#     """
#     post:
#     Create a new Desk instance
#     """
#     is_json = True
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
#
#     def list(self, request, *args, **kwargs):
#         qs = Desk.objects.all()
#         json_data = qs.serialize()
#
#         return self.render_to_response(json_data)
#
#     def create(self, request, *args, **kwargs):
#
#         form = DeskModelForm(request.POST)
#         if form.is_valid():
#             obj = Desk.objects.create(author=request.user, name=request.POST["name"],
#                                       description=request.POST["description"])
#
#             basic_group = CustomGroup.objects.create(name="POOL_" + obj.name + "_" + str(obj.id),
#                                                      related_desk=obj)
#
#             editor_group = CustomGroup.objects.create(name="EDITOR_" + obj.name + "_" + str(obj.id),
#                                                       related_desk=obj)
#
#             staff_group = CustomGroup.objects.create(name="STAFF_" + obj.name + "_" + str(obj.id),
#                                                      related_desk=obj)
#             basic_group.save()
#             editor_group.save()
#             staff_group.save()
#             obj.save()
#             obj_data = obj.serialize()
#             return self.render_to_response(obj_data)
#         if form.errors:
#             data = json.dumps(form.errors)
#             return self.render_to_response(data, 400)
#         data = {'error': 'Not Allowed'}
#         return self.render_to_response(data, 403)


# class DeskAPIView(generics.ListAPIView):
#     permission_classes = []
#     authentication_classes = []
#     serializer_class = DeskSerializer
#
#
#     def get(self, request, format=None):
#         qs = Desk.objects.all()
#         serializer = DeskSerializer(qs, many=True)
#         return Response(serializer.data)


def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid


class DeskAPIView(generics.ListAPIView,
                  mixins.CreateModelMixin,
                  ):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = DeskSerializer
    passed_id = None
    queryset = Desk.objects.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    # def perform_destroy(self, instance):
    #     if instance is not None:
    #         return instance.delete()
    #     return None

    # def get_queryset(self):
    #     request = self.request
    #     qs = Desk.objects.all()
    #     query = request.GET.get('q')
    #     if query is not None:
    #         qs = qs.filter(content__icontatins=query)
    #     return qs

    # def get_object(self):
    #     request = self.request
    #     passed_id = request.GET.get('id')
    #     query_set = self.get_queryset()
    #     obj = None
    #     if passed_id is not None:
    #         obj = get_object_or_404(query_set, id=passed_id)
    #         self.check_object_permissions(request, obj)
    #     return obj

    # TODO
    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #     desks = user.usersdesks_set.all()
    #     print(len(desks))
    #     serializer = self.get_serializer(desks, many=True)
    #     json_data = serializer.data
    #     #json_data = serializers.serialize('json', desks)
    #     #json_data = json_data.data
    #     return Response(json_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # create Desk object
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        desk_object = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # create relation between user and desk
        rel = UsersDesks.objects.create(user=request.user, desks=desk_object)
        rel.save()

        p = PermissionRow.objects.create(related_desk=desk_object, user=request.user, permission="ADMIN")
        p.save()

        # # create pool groups for permissions
        # staff_group = CustomGroup.objects.create(name="STAFF_" + desk_object.name + "_" + str(desk_object.id),
        #                                          related_desk=desk_object)
        #
        # editor_group = CustomGroup.objects.create(name="EDITOR_" + desk_object.name + "_" + str(desk_object.id),
        #                                           related_desk=desk_object)
        #
        # # add all participants of the desk here
        # common_group = CustomGroup.objects.create(name="COMMON_" + desk_object.name + "_" + str(desk_object.id),
        #                                           related_desk=desk_object)
        #
        # staff_group.save()
        # editor_group.save()
        # common_group.save()

        # return success response
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class DeskCreateAPIView(generics.CreateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Desk.objects.all()
#     serializer_class = DeskSerializer

# def get_queryset(self):
#     qs = Desk.objects.all()
#     query = self.request.GET.get('q')
#     if query is not None:
#         qs = qs.filter(content__icontatins=query)
#     return qs


class DeskDetailAPIView(mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.RetrieveAPIView,
                        ):
    permission_classes = [permissions.IsAuthenticated, IsEditorOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    queryset = Desk.objects.all()
    serializer_class = DeskSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#class AddUserWithPermissionsAPIView(generics)