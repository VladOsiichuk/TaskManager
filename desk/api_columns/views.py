from desk.model import Column, Desk
from .serializers import ColumnSerializer
from rest_framework import generics
from rest_framework import mixins, permissions
from rest_framework.authentication import SessionAuthentication
from api_rules.permissions import IsEditorOfDeskOrHigher
from rest_framework import status
from rest_framework.response import Response


class ColumnAPIView(generics.CreateAPIView,
                    generics.ListAPIView
                    ):

    permission_classes = [permissions.IsAuthenticated, IsEditorOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    serializer_class = ColumnSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'column_id'
    queryset = Column.objects.prefetch_related("tasks__comments").all()

    # disable pagination
    paginator = None

    def get(self,  request, *args, **kwargs):

        desk = Desk.objects.prefetch_related("permissionrow_set__user").filter(id=self.kwargs['desk_id']).first()
        self.check_object_permissions(self.request, desk)

        queryset = self.queryset.filter(related_desk=desk)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        desk_id = self.kwargs["desk_id"]
        return serializer.save(author=self.request.user, related_desk_id=desk_id)

    def post(self, request, *args, **kwargs):

        # check if user has access to create a new column
        desk = Desk.objects.get(id=self.kwargs["desk_id"])
        self.check_object_permissions(request, desk)

        # create Column object
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        # return success response
        return Response(serializer.data, status=201)


class ColumnDetailAPIView(mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          generics.RetrieveAPIView,
                          ):
    permission_classes = [permissions.IsAuthenticated, IsEditorOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'column_id'

    def get(self, request, *args, **kwargs):
        instance = Column.objects.prefetch_related("tasks__comments__related_comment")\
            .get(id=self.kwargs['column_id'])

        #select_related("related_desk").filter(id=self.kwargs["column_id"]).first()
        if instance.related_desk_id != self.kwargs["desk_id"]:
            return Response({"detail": "not found"}, status=404)
        print(request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
