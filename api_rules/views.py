from .permissions import IsAdminOfDesk, IsEditorOfDesk, IsStaffOfDesk
from rest_framework.views import APIView
from .serializers import UpdateUserPermissionsSerializer, AddUserToDeskSerializer
from user_auth.models import CustomGroup
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics
from desk.model import Desk
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import mixins

User = get_user_model()


class AddUserWithPermissionsAPIView(#generics.CreateAPIView,
                                    #generics.ListAPIView,
                                    #generics.RetrieveAPIView,
                                    #generics.UpdateAPIView,
                                    #generics.ListAPIView,
                                    generics.CreateAPIView
                                   ):

    authentication_classes = [SessionAuthentication]
    permission_classes = []
    serializer_class = AddUserToDeskSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        desk_id = self.kwargs.get('desk_id')
        u = User.objects.get(id=self.kwargs.get('id'))
        data = request.data
        add_to = request.data.get('desk_name')
        part_name = add_to.upper() + "_" + str(desk_id)
        print(part_name)
        group = Desk.objects.get(id=desk_id).customgroup_set.all()
        print(type(group))
        group = group.filter(name__contains=add_to.upper()).first()

        group.user_set.add(u)

        return Response(status=200)


    # def update(self, request, *args, **kwargs):
    #     #self.permission_classes = [IsEditorOfDesk]
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(serializer.data)
    # def get_object(self):
    #     id = self.request.GET.get('pk')
    #     print(id)
    #     #qs = Desk.objects.get(id=id).customgroup_set.all()
    #     return CustomGroup.objects.first()
    # def post(self, request, *args, **kwargs):
    #     data = request.data
    # def post(self, request, *args, **kwargs):
    #     """
    #     If you add user for the first time(It means user was not participant of this desk before)
    #     then use POST method
    #     """
    #     data = request.data
    #
    #     user_id = data.get("user_id")
    #     desk_id = data.get("desk_id")
    #     add_to = data.get("change_to_permission")
    #
    #     desk = Desk.objects.filter(id=desk_id).first()
    #
    #     if not desk:
    #         return Response({"error": "Desk with that name does not exists"}, status=400)
    #
    #     if desk.author_id == user_id:
    #         return Response({"error": "You cannot change admin user role"}, status=403)
    #
    #     user = User.objects.filter(id=user_id).first()
    #     part_group_name = desk.name + "_" + str(desk.id)
    #     print(add_to.upper() + "_" + part_group_name)
    #     participants_group = CustomGroup.objects.get(name="COMMON" + "_" + part_group_name)
    #     group_to_add = CustomGroup.objects.get(name=add_to.upper() + "_" + part_group_name)
    #
    #     participants_group.user_set.add(user)
    #     group_to_add.user_set.add(user)
    #
    #     return Response(status=200)
    # def put(self, request, *args, **kwargs):
    #     """
    #     If you want to change user's rules in the desk (It means user is already
    #     participant of this desk) then use PATCH method
    #     """
    #     data = request.data
    #
    #     user_id = data.get("user_id")
    #     desk_id = data.get("desk_id")
    #     change_from = data.get("change_from_permission")
    #     change_to = data.get("change_to_permission")
    #
    #     desk = Desk.objects.filter(id=desk_id).first()
    #
    #     if not desk:
    #         return Response({"error": "Desk with that id does not exists"}, status=400)
    #
    #     if desk.author_id == user_id:
    #         return Response({"error": "You cannot change admin user role"}, status=403)
    #
    #     user = User.objects.filter(id=user_id).first()
    #     part_group_name = desk.name + "_" + str(desk.id)
    #
    #     group_to_add = CustomGroup.objects.get(name=change_to.upper() + "_" + part_group_name)
    #
    #     delete_from_group = CustomGroup.objects.get(name=change_from.upper() + "_" + part_group_name)
    #     delete_from_group.user_set.remove(user)
    #
    #     group_to_add.user_set.add(user)
    #
    #     return Response(status=200)
    #
    # def delete(self, request, *args, **kwargs):
    #     """Just provide user_id and desk_id"""
    #     data = request.data
    #
    #     user_id = data.get("user_id")
    #     desk_id = data.get("desk_id")
