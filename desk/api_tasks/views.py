from desk.model import Column, Desk, Task
from .serializers import CreateTaskSerializer, UpdateTaskSerializer
from rest_framework import generics
from rest_framework import mixins, permissions
from rest_framework.authentication import SessionAuthentication
from api_rules.permissions import IsEditorOfDeskOrHigher
from rest_framework import status
from rest_framework.response import Response


class TaskAPIView(generics.CreateAPIView,
                  generics.ListAPIView
                  ):

    permission_classes = [permissions.IsAuthenticated, IsEditorOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    serializer_class = CreateTaskSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'
#    queryset = Task.objects.all()

    def get_queryset(self, *args, **kwargs):
        #print(self.kwargs['id'])
        qs = Task.objects.select_related('related_column__related_desk').filter(related_column_id=self.kwargs['column_id'])
        return qs #self.queryset.filter(related_column_id=self.kwargs['column_id'])

    def perform_create(self, serializer):
        column_id = self.kwargs["column_id"]
        return serializer.save(related_column_id=column_id)

    def post(self, request, *args, **kwargs):
        """
        Creates a new Task.
        """
        # check if user has access to create a new task
        column = Column.objects.get(id=self.kwargs["column_id"])

        # if provided id is incorrect
        if not column:
            return Response({"error": "invalid column id"}, status=400)

        # check if user has access to create a new task
        self.check_object_permissions(request, column)

        # create Task object
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        # return success response
        return Response(serializer.data, status=201)


class TaskDetailAPIView(mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.RetrieveAPIView,
                        ):

    permission_classes = [permissions.IsAuthenticated, IsEditorOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    queryset = Task.objects.all().prefetch_related("comments__author")
    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'
    serializer_class = UpdateTaskSerializer

    def get(self, request, *args, **kwargs):
        """
        Get information about task with ID=task_id. If Task is not related to the
        Column with ID=column_id then 404 error
        """
        instance = self.get_object()
        #instance = Task.objects.select_related("related_column").prefetch_related("comments__parent__author").filter(id=self.kwargs[self.lookup_url_kwarg]).first()
        if instance.related_column_id != self.kwargs["column_id"]:
            return Response({"detail": "not found"}, status=404)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return Response({"message": "please use PATCH method instead"}, status=400)

    def put(self, request, *args, **kwargs):
        """
        Updates the Task. Allowed only to EDITOR, ADMIN and person for who task is assigned
        """
        partial = kwargs.pop('partial', False)

        # Check if selected column is related to the Current Desk
        desk_id = self.kwargs["desk_id"]
        related_column_id = int(request.data['related_column'])
        print(related_column_id, desk_id)
        col = Column.objects.get(id=related_column_id)

        # if desk_id is not the same as related_desk_id then return Bad Response
        if col.related_desk_id != desk_id:
            return Response({"Message": f"Selected column(ID={related_column_id})"
                            f" is not related to the desk with ID={related_column_id}"}, status=400)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def delete(self, request, *args, **kwargs):
        """
        Delete task which has task_id
        """
        return self.destroy(request, *args, **kwargs)
